/** @type {import('next').NextConfig} */
const nextConfig = {
  distDir: '.next',
  output: 'standalone',
  reactStrictMode: true,
  images: {
    // Serve original URLs (no /_next/image optimizer) — matches standalone Docker runner
    unoptimized: true,
    remotePatterns: [
      {
        protocol: 'http',
        hostname: 'localhost',
        pathname: '/**',
      },
      {
        protocol: 'https',
        hostname: 'localhost',
        pathname: '/**',
      },
    ],
  },
  async rewrites() {
    return [
      // Browser or cached bundles may still call /api/v1/auth/* (Flask path). Map to Next proxies.
      {
        source: '/api/v1/auth/:path*',
        destination: '/api/auth/:path*',
      },
      {
        // Properly handle DOCiD identifiers with slashes
        source: '/docid/:slug*',
        destination: '/docid/:slug*',
      },
    ];
  },
  // Use this to handle special characters in URL paths
  trailingSlash: false,
};

module.exports = nextConfig;