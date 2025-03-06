// Deno development server
import { serve } from "std/http/server.ts";
import { serveDir } from "std/http/file_server.ts";

const PORT = 3000;
console.log(`Starting development server at http://localhost:${PORT}`);

serve(async (req) => {
  const url = new URL(req.url);
  
  // API proxy for backend requests
  if (url.pathname.startsWith("/api")) {
    const apiUrl = new URL(url.pathname.replace(/^\/api/, ""), "http://localhost:8000");
    console.log(`Proxying request to: ${apiUrl}`);
    
    const apiReq = new Request(apiUrl, {
      method: req.method,
      headers: req.headers,
      body: req.body
    });
    
    try {
      return await fetch(apiReq);
    } catch (error) {
      console.error("API proxy error:", error);
      return new Response(JSON.stringify({ error: "Backend connection failed" }), {
        status: 502,
        headers: { "Content-Type": "application/json" }
      });
    }
  }
  
  // Serve static files
  return await serveDir(req, {
    fsRoot: ".",
    urlRoot: "",
    showDirListing: true,
    enableCors: true,
  });
}, { port: PORT }); 