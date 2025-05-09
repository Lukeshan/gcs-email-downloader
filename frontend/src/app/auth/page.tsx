"use client";

import { useEffect, useState } from "react";
import Dropdown from "../../components/Dropdown"; 

async function fetchLabels() {
  try {
    const response = await fetch("http://127.0.0.1:5000/listlabels"); // Calls the Next.js API route
    if (response.ok) { 
      const data = await response.json()
      return data["labels"]
    } else {
      console.error("Error fetching token:", response.status, response.statusText);
      return []
    }
  } catch (error) {
    console.error("Request failed:", error);
    return []
  }
}
  


export default function Auth() {
  const [currentUrl, setCurrentUrl] = useState<string>("");
  const [selectedValue, setSelectedValue] = useState<string>("");
  const [isVisible, setIsVisible] = useState<boolean>(true);
  const [labels, setLabels] = useState<string[]>([]);
  
  useEffect(() => {
    setCurrentUrl(window.location.href);
  }, []);
  return (
    <main className="p-4">
      <h1 className="text-xl font-bold">Authentication</h1>
      <button onClick={() => window.location.href = `http://127.0.0.1:5000/authredirect?redirect_url=${currentUrl}`} className="px-2 py-1 bg-blue-500 text-white rounded hover:bg-blue-700">Test Auth</button>
      <button onClick={async () => setLabels(await fetchLabels())} className="px-2 py-1 bg-green-500 text-white rounded hover:bg-green-700">test token</button>
      <p>Here you can log in or sign up.</p>
      {/* Fixing prop syntax */}
      <Dropdown options={labels} isVisible={isVisible} selectedValue={selectedValue} setSelectedValue={setSelectedValue} />
      <br/>
      <p className="text-xl text-green-300">{selectedValue}</p>
    </main>
  );
}
