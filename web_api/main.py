"""
FastAPI web application for AI Co-pilot
"""

import asyncio
from typing import Dict, List, Optional, Any
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn
import logging

from ai_copilot import AICopilot, CopilotConfig
from ai_copilot.core import CodeRequest


# Pydantic models for API
class CodeGenerationRequest(BaseModel):
    description: str
    language: str = "c"
    target_platform: Optional[str] = None
    constraints: Optional[Dict[str, Any]] = None


class CodeAnalysisRequest(BaseModel):
    code: str
    language: str = "c"


class CodeGenerationResponse(BaseModel):
    generated_code: str
    explanation: str
    warnings: List[str]
    suggestions: List[str]
    metadata: Dict[str, Any]


class CodeAnalysisResponse(BaseModel):
    warnings: List[str]
    suggestions: List[str]
    metrics: Dict[str, Any]
    is_valid: bool


class StatusResponse(BaseModel):
    status: str
    message: str
    version: str = "0.1.0"


# Initialize FastAPI app
app = FastAPI(
    title="AI Co-pilot for Embedded Software Design",
    description="Generate, analyze, and optimize embedded software for smart vehicles",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global AI Co-pilot instance
copilot: Optional[AICopilot] = None


@app.on_event("startup")
async def startup_event():
    """Initialize the AI Co-pilot on startup"""
    global copilot
    
    try:
        config = CopilotConfig()
        config.log_level = "INFO"
        
        copilot = AICopilot(config)
        await copilot.initialize()
        
        logging.info("AI Co-pilot web API started successfully")
        
    except Exception as e:
        logging.error(f"Failed to initialize AI Co-pilot: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global copilot
    
    if copilot:
        copilot.shutdown()
        logging.info("AI Co-pilot web API shutdown complete")


# API Routes
@app.get("/api/status", response_model=StatusResponse)
async def get_status():
    """Get API status"""
    return StatusResponse(
        status="running" if copilot and copilot.is_initialized else "initializing",
        message="AI Co-pilot API is operational"
    )


@app.post("/api/generate", response_model=CodeGenerationResponse)
async def generate_code(request: CodeGenerationRequest):
    """Generate code based on description"""
    global copilot
    
    if not copilot or not copilot.is_initialized:
        raise HTTPException(status_code=503, detail="AI Co-pilot not initialized")
    
    try:
        # Create code request
        code_request = CodeRequest(
            description=request.description,
            language=request.language,
            target_platform=request.target_platform,
            constraints=request.constraints
        )
        
        # Generate code
        response = await copilot.generate_code(code_request)
        
        return CodeGenerationResponse(
            generated_code=response.generated_code,
            explanation=response.explanation,
            warnings=response.warnings,
            suggestions=response.suggestions,
            metadata=response.metadata
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Code generation failed: {str(e)}")


@app.post("/api/analyze", response_model=CodeAnalysisResponse)
async def analyze_code(request: CodeAnalysisRequest):
    """Analyze existing code"""
    global copilot
    
    if not copilot or not copilot.is_initialized:
        raise HTTPException(status_code=503, detail="AI Co-pilot not initialized")
    
    try:
        # Analyze code
        analysis = await copilot.analyze_existing_code(request.code, request.language)
        
        return CodeAnalysisResponse(
            warnings=analysis.get('warnings', []),
            suggestions=analysis.get('suggestions', []),
            metrics=analysis.get('metrics', {}),
            is_valid=analysis.get('is_valid', True)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Code analysis failed: {str(e)}")


@app.get("/api/suggestions")
async def get_code_suggestions(partial_code: str, cursor_position: int = 0):
    """Get code completion suggestions"""
    global copilot
    
    if not copilot or not copilot.is_initialized:
        raise HTTPException(status_code=503, detail="AI Co-pilot not initialized")
    
    try:
        suggestions = await copilot.get_suggestions(partial_code, cursor_position)
        return {"suggestions": suggestions}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get suggestions: {str(e)}")


@app.get("/api/templates")
async def get_templates():
    """Get available code templates"""
    try:
        from code_generation.templates import TemplateManager
        
        template_manager = TemplateManager()
        templates = template_manager.list_templates()
        
        return {"templates": templates}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get templates: {str(e)}")


@app.get("/api/platforms")
async def get_platforms():
    """Get supported platforms"""
    try:
        from embedded_integration.platforms import PlatformManager
        
        config = CopilotConfig()
        platform_manager = PlatformManager(config)
        
        platforms = list(platform_manager.platforms.keys())
        
        return {"platforms": platforms}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get platforms: {str(e)}")


# Serve static files (React app) - only if directory exists
import os
if os.path.exists("web_frontend/build/static"):
    app.mount("/static", StaticFiles(directory="web_frontend/build/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serve the React frontend"""
    try:
        if os.path.exists("web_frontend/build/index.html"):
            with open("web_frontend/build/index.html", "r") as f:
                return HTMLResponse(content=f.read())
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        return HTMLResponse(
            content="""
            <!DOCTYPE html>
            <html>
                <head>
                    <title>AI Co-pilot for Embedded Software Design</title>
                    <style>
                        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                        .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                        h1 { color: #1890ff; margin-bottom: 20px; }
                        .api-link { display: inline-block; background: #1890ff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; margin: 10px 5px; }
                        .api-link:hover { background: #40a9ff; }
                        .feature { background: #f9f9f9; padding: 15px; margin: 10px 0; border-radius: 4px; }
                        .status { color: #52c41a; font-weight: bold; }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>🚗 AI Co-pilot for Embedded Software Design</h1>
                        <p class="status">✓ Backend API is running successfully!</p>

                        <h2>Available API Endpoints:</h2>
                        <a href="/api/docs" class="api-link">📚 Interactive API Documentation</a>
                        <a href="/api/redoc" class="api-link">📖 ReDoc Documentation</a>

                        <h2>Features:</h2>
                        <div class="feature">
                            <strong>🔧 Code Generation:</strong> Generate embedded C/C++ code for automotive applications
                        </div>
                        <div class="feature">
                            <strong>🔍 Code Analysis:</strong> Analyze existing code for embedded constraints and safety compliance
                        </div>
                        <div class="feature">
                            <strong>🚗 Vehicle Context:</strong> Automotive-specific knowledge for ECUs, protocols, and standards
                        </div>
                        <div class="feature">
                            <strong>⚡ Real-time Constraints:</strong> Memory, timing, and safety analysis for embedded systems
                        </div>

                        <h2>Quick Start:</h2>
                        <p>Try the API endpoints above, or use the command line interface:</p>
                        <pre style="background: #f0f0f0; padding: 15px; border-radius: 4px;">
python -m ai_copilot.cli generate "Create CAN message handler"
python -m ai_copilot.cli analyze my_code.c
python -m ai_copilot.cli interactive</pre>

                        <h2>React Frontend:</h2>
                        <p>To build and run the full web interface:</p>
                        <pre style="background: #f0f0f0; padding: 15px; border-radius: 4px;">
cd web_frontend
npm install
npm run build
# Then restart this server</pre>
                    </div>
                </body>
            </html>
            """
        )


if __name__ == "__main__":
    uvicorn.run(
        "web_api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
