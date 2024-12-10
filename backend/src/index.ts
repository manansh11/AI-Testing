import express from 'express'
import dotenv from 'dotenv'
import { testConnection } from './utils/aptos'

dotenv.config()

const app = express()
const port = process.env.PORT || 3001

app.use(express.json())

app.get('/api/health', async (req, res) => {
  const isConnected = await testConnection()
  res.json({
    status: 'ok',
    aptosConnection: isConnected
  })
})

app.listen(port, () => {
  console.log(`Server running on port ${port}`)
})
