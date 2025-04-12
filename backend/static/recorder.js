let mediaRecorder;
let audioChunks = [];


async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
            audio: {
                channelCount: 1,
                sampleRate: 16000,
                echoCancellation: true,
                noiseSuppression: true
            } 
        });
        
        const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus') 
            ? 'audio/webm;codecs=opus'
            : 'audio/webm';
            
        mediaRecorder = new MediaRecorder(stream, {
            mimeType: mimeType,
            audioBitsPerSecond: 16000
        });
        audioChunks = [];

        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
                console.log(`Received chunk of size: ${event.data.size}`);
            }
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: mimeType });
            console.log(`Total audio size: ${audioBlob.size} bytes`);
            
            const formData = new FormData();
            formData.append('audio', audioBlob, 'recording.webm');
            
            try {
                console.log('Sending audio to server...');
                const response = await fetch('/transcribe', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    const data = await response.json();
                    if (data.transcript) {
                        document.getElementById("question").value = data.transcript;
                        console.log('Received transcript:', data.transcript);
                    } else {
                        console.error('No transcript received');
                    }
                } else {
                    const errorData = await response.json();
                    console.error('Transcription failed:', errorData.error);
                }
            } catch (error) {
                console.error('Error sending audio:', error);
            }
        };

        mediaRecorder.start(1000); // Collect data every second
        console.log("Recording started with MIME type:", mimeType);
    } catch (error) {
        console.error("Error accessing microphone:", error);
    }
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
        mediaRecorder.stop();
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
        console.log("Recording stopped");
    }
}