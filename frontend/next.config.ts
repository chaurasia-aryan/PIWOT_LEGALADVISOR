/** @type {import('next').NextConfig} */
const nextConfig = {
  rewrites: async () => {
    return [
      {
        source: '/api/:path*',
        destination:
          process.env.NODE_ENV === 'development'
            ? 'http://172.22.33.146:3000/api/:path*'
            : '/api/',
      },
    ]
  },
}

module.exports = nextConfig