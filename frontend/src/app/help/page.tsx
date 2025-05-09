"use client";

async function buttonPressed() {
  try {
    const response = await fetch("http://127.0.0.1:5001/test"); // Calls the Next.js API route
    if (response.ok) {
      console.log("All good at end")
      const data = await response.json()
      console.log(data["name"])
    } else {
      console.error("Error fetching token:", response.status, response.statusText);
    }
  } catch (error) {
    console.error("Request failed:", error);
  }
}

export default function Help() {
  return (
    <main className="p-4">
      <h1 className="text-xl font-bold">Help & Support</h1>
      <button onClick={buttonPressed} className="px-2 py-1 bg-pink-500 text-white rounded hover:bg-pink-700">Get test</button>
      <p>Need help? Reach out to support.</p>
    </main>
  );
}
