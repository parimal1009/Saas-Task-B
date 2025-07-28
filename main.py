from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from datetime import datetime
import json
import os
from typing import Optional
from mangum import Mangum

app = FastAPI(title="NeuralFlow SaaS", description="The Future of Business Intelligence")

# Add CORS middleware for Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Gzip compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Create templates directory if it doesn't exist
if not os.path.exists("templates"):
    os.makedirs("templates")

# Create static directory if it doesn't exist
if not os.path.exists("static"):
    os.makedirs("static")

templates = Jinja2Templates(directory="templates")

# Mount static files (for local development)
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception:
    # Vercel handles static files differently
    pass

# Data models
class ContactForm(BaseModel):
    name: str
    email: EmailStr
    company: Optional[str] = None
    message: str

class NewsletterSignup(BaseModel):
    email: EmailStr

class DemoRequest(BaseModel):
    name: str
    email: EmailStr
    company: str
    phone: Optional[str] = None
    employees: str
    use_case: str

# In-memory storage (replace with database in production)
contacts = []
newsletter_subscribers = []
demo_requests = []

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main landing page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    """Health check endpoint for Vercel"""
    return {
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "service": "NeuralFlow SaaS",
        "platform": "Vercel"
    }

@app.post("/api/contact")
async def submit_contact(contact: ContactForm):
    """Handle contact form submissions"""
    contact_data = contact.dict()
    contact_data["timestamp"] = datetime.now().isoformat()
    contacts.append(contact_data)
    
    return JSONResponse({
        "status": "success",
        "message": "Thank you for your message! We'll get back to you within 24 hours.",
        "data": contact_data
    })

@app.post("/api/newsletter")
async def subscribe_newsletter(signup: NewsletterSignup):
    """Handle newsletter subscriptions"""
    # Check if email already exists
    if any(sub["email"] == signup.email for sub in newsletter_subscribers):
        raise HTTPException(status_code=400, detail="Email already subscribed")
    
    subscriber_data = signup.dict()
    subscriber_data["timestamp"] = datetime.now().isoformat()
    newsletter_subscribers.append(subscriber_data)
    
    return JSONResponse({
        "status": "success",
        "message": "🎉 Welcome to the future! You're now subscribed to our newsletter.",
        "subscriber_count": len(newsletter_subscribers)
    })

@app.post("/api/demo")
async def request_demo(demo: DemoRequest):
    """Handle demo requests"""
    demo_data = demo.dict()
    demo_data["timestamp"] = datetime.now().isoformat()
    demo_requests.append(demo_data)
    
    return JSONResponse({
        "status": "success",
        "message": "🚀 Demo request received! Our team will contact you within 2 hours to schedule your personalized demo.",
        "data": demo_data
    })

@app.get("/api/stats")
async def get_stats():
    """Get platform statistics for dynamic content"""
    return JSONResponse({
        "total_users": "50,000+",
        "companies_served": "1,200+",
        "data_processed": "2.5TB",
        "uptime": "99.99%",
        "newsletter_subscribers": len(newsletter_subscribers),
        "demo_requests": len(demo_requests),
        "contact_submissions": len(contacts)
    })

@app.get("/api/features")
async def get_features():
    """Get dynamic feature list"""
    features = [
        {
            "id": 1,
            "title": "AI-Powered Analytics",
            "description": "Leverage machine learning to uncover hidden insights in your data with real-time predictive analytics.",
            "icon": "🧠",
            "category": "Analytics"
        },
        {
            "id": 2,
            "title": "Real-Time Dashboards",
            "description": "Beautiful, interactive dashboards that update in real-time with stunning visualizations.",
            "icon": "📊",
            "category": "Visualization"
        },
        {
            "id": 3,
            "title": "Advanced Security",
            "description": "Enterprise-grade security with end-to-end encryption and compliance with SOC 2, GDPR, and HIPAA.",
            "icon": "🔒",
            "category": "Security"
        },
        {
            "id": 4,
            "title": "Cloud Integration",
            "description": "Seamlessly connect with 100+ cloud services and APIs with zero-configuration setup.",
            "icon": "☁️",
            "category": "Integration"
        },
        {
            "id": 5,
            "title": "Smart Automation",
            "description": "Intelligent workflow automation that learns from your patterns and optimizes processes.",
            "icon": "⚡",
            "category": "Automation"
        },
        {
            "id": 6,
            "title": "Collaborative Workspaces",
            "description": "Real-time collaboration tools with comments, sharing, and team management features.",
            "icon": "👥",
            "category": "Collaboration"
        }
    ]
    return JSONResponse({"features": features})

@app.get("/api/testimonials")
async def get_testimonials():
    """Get customer testimonials"""
    testimonials = [
        {
            "id": 1,
            "name": "Sarah Chen",
            "role": "CTO",
            "company": "TechFlow Inc.",
            "avatar": "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=100&h=100&fit=crop&crop=face",
            "content": "NeuralFlow transformed our data strategy completely. The AI insights helped us increase revenue by 40% in just 3 months.",
            "rating": 5
        },
        {
            "id": 2,
            "name": "Marcus Rodriguez",
            "role": "Data Director",
            "company": "Global Dynamics",
            "avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop&crop=face",
            "content": "The real-time dashboards are incredible. Our team makes faster, smarter decisions every single day.",
            "rating": 5
        },
        {
            "id": 3,
            "name": "Emily Watson",
            "role": "VP Analytics",
            "company": "InnovateCorp",
            "avatar": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&h=100&fit=crop&crop=face",
            "content": "Implementation was seamless, and the ROI was visible within weeks. This is the future of business intelligence.",
            "rating": 5
        }
    ]
    return JSONResponse({"testimonials": testimonials})

@app.get("/api/pricing")
async def get_pricing():
    """Get pricing plans"""
    plans = [
        {
            "id": "starter",
            "name": "Starter",
            "price": 29,
            "billing": "per month",
            "description": "Perfect for small teams getting started",
            "features": [
                "Up to 5 team members",
                "10GB data storage",
                "Basic analytics",
                "Email support",
                "Standard dashboards"
            ],
            "popular": False,
            "cta": "Start Free Trial"
        },
        {
            "id": "professional",
            "name": "Professional",
            "price": 89,
            "billing": "per month",
            "description": "Advanced features for growing companies",
            "features": [
                "Up to 25 team members",
                "100GB data storage",
                "AI-powered insights",
                "Priority support",
                "Custom dashboards",
                "API access",
                "Advanced integrations"
            ],
            "popular": True,
            "cta": "Start Free Trial"
        },
        {
            "id": "enterprise",
            "name": "Enterprise",
            "price": 299,
            "billing": "per month",
            "description": "Full-scale solution for large organizations",
            "features": [
                "Unlimited team members",
                "Unlimited data storage",
                "Advanced AI & ML",
                "24/7 dedicated support",
                "White-label solution",
                "Custom integrations",
                "SLA guarantee",
                "On-premise deployment"
            ],
            "popular": False,
            "cta": "Contact Sales"
        }
    ]
    return JSONResponse({"plans": plans})

# Create the handler for Vercel
handler = Mangum(app)