import React, { useEffect, useState } from 'react'
import { Box, Typography, Container } from '@mui/material'
import { testConnection } from '../utils/aptos'

export default function Home() {
  const [connected, setConnected] = useState<boolean | null>(null)

  useEffect(() => {
    const checkConnection = async () => {
      const isConnected = await testConnection()
      setConnected(isConnected)
    }
    checkConnection()
  }, [])

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          NFT Platform
        </Typography>
        <Typography variant="body1" gutterBottom>
          Aptos Connection Status: {connected === null ? 'Checking...' : connected ? 'Connected' : 'Not Connected'}
        </Typography>
      </Box>
    </Container>
  )
}
