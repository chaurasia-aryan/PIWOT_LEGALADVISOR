import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    status: 'healthy',
    mode: 'vercel-serverless',
    engine: 'PIWOT Legal Advisor 2.0 (Hybrid Serverless & Remote ML Proxy)',
    categories: 12,
    timestamp: new Date().toISOString(),
  });
}
