import { NextResponse } from 'next/server';
import { BACKEND_API_URL } from '@/lib/backendUrl';

/**
 * Browser calls same-origin /api/auth/login so traffic hits Next, then Flask on the Docker network.
 * Avoids nginx sending /api/v1/* to the wrong upstream.
 */
export async function POST(request) {
  try {
    const body = await request.json();
    const response = await fetch(`${BACKEND_API_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const data = await response.json().catch(() => ({}));
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error('auth/login proxy:', error);
    return NextResponse.json(
      { error: 'An error occurred during sign in. Please try again.' },
      { status: 500 }
    );
  }
}

export async function OPTIONS() {
  return new NextResponse(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  });
}
