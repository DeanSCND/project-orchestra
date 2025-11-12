export const runtime = 'edge';

export async function GET() {
  return new Response('Auth temporarily disabled for MVP', { status: 404 });
}

export async function POST() {
  return new Response('Auth temporarily disabled for MVP', { status: 404 });
}
