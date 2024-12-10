/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    APTOS_NODE_URL: process.env.APTOS_NODE_URL || 'https://fullnode.testnet.aptoslabs.com/v1',
    APTOS_FAUCET_URL: process.env.APTOS_FAUCET_URL || 'https://faucet.testnet.aptoslabs.com',
    IPFS_NODE_URL: process.env.IPFS_NODE_URL || 'https://ipfs.infura.io:5001'
  }
}

module.exports = nextConfig
