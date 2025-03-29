async function fetchLatest() {
    try {
      const res = await fetch("http://localhost:8000/latest");
      const data = await res.json();
      document.getElementById("output").textContent = data.response || "No response yet.";
    } catch (err) {
      console.error("Error fetching latest response:", err);
    }
  }
  
  // Poll every 3 seconds
  setInterval(fetchLatest, 3000);
  