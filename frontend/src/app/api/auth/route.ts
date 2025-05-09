import { NextRequest, NextResponse } from "next/server";

export async function GET(req: NextRequest) {
  const flaskURL = "http://127.0.0.1:5000/retrievetoken"; // Get token from Flask session
  const res = await fetch(flaskURL);
  
  if (res.ok) {
    const data = await res.json();
    return NextResponse.json(data); // Return token JSON
  } else {
    return NextResponse.json({ error: "Failed to retrieve token" }, { status: res.status });
  }
}
