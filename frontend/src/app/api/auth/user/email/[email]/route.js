import { NextResponse } from 'next/server';
import { BACKEND_API_URL } from '@/lib/backendUrl';

export async function GET(request, { params }) {
  try {
    const { email: emailSegment } = await params;
    const email = decodeURIComponent(emailSegment);
    const url = `${BACKEND_API_URL}/auth/user/email/${encodeURIComponent(email)}`;
    const response = await fetch(url, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    const data = await response.json().catch(() => ({}));
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error('auth/user/email proxy:', error);
    return NextResponse.json({ message: 'Failed to fetch user' }, { status: 500 });
  }
}
