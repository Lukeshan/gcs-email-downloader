import { NextRequest, NextResponse } from "next/server";

export async function GET(req: NextRequest) {
  const flaskURL = "http://127.0.0.1:5000/checktoken"; // Get token from Flask session
  const res = await fetch(flaskURL);
  const data = await res.json()
  console.log(data)
  if (res.ok) {
    return NextResponse.json({data: data},{status : res.status}); // Return token JSON
  } else {
    return NextResponse.json({ error: "Failed to retrieve token" }, { status: res.status });
  }
}
