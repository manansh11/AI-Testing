# Build Instructions and Code Style Guidelines

## Prerequisites

### Development Tools
```bash
# Node.js and npm
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Yarn (optional but recommended)
npm install -g yarn

# TypeScript
npm install -g typescript

# Aptos CLI
curl -fsSL "https://aptos.dev/scripts/install_cli.py" | python3

# IPFS (for metadata storage)
wget https://dist.ipfs.tech/kubo/v0.17.0/kubo_v0.17.0_linux-amd64.tar.gz
tar -xvzf kubo_v0.17.0_linux-amd64.tar.gz
cd kubo
sudo bash install.sh
```

### Environment Setup
1. Clone the repository
```bash
git clone https://github.com/manansh11/AI-Testing.git
cd AI-Testing
```

2. Install dependencies
```bash
# Install frontend dependencies
cd frontend
yarn install

# Install backend dependencies
cd ../backend
yarn install
```

3. Configure environment variables
```bash
# Create .env files
cp .env.example .env
```

## Project Structure
```
AI-Testing/
├── frontend/           # React.js frontend application
├── backend/           # Node.js backend server
├── contracts/         # Move smart contracts
├── scripts/          # Deployment and utility scripts
└── docs/             # Documentation
```

## Smart Contract Development

### Contract Compilation
```bash
# Navigate to contracts directory
cd contracts

# Compile Move contracts
aptos move compile
```

### Contract Testing
```bash
# Run Move tests
aptos move test

# Run test coverage
aptos move coverage
```

### Contract Deployment
```bash
# Deploy to testnet
aptos move publish --named-addresses nft_token=default
```

## Frontend Development

### Development Server
```bash
cd frontend
yarn dev
```

### Production Build
```bash
yarn build
yarn start
```

### Environment Configuration
Required environment variables:
```env
APTOS_NODE_URL=https://fullnode.testnet.aptoslabs.com/v1
APTOS_FAUCET_URL=https://faucet.testnet.aptoslabs.com
IPFS_NODE_URL=https://ipfs.infura.io:5001
```

## Backend Development

### Development Server
```bash
cd backend
yarn dev
```

### Production Build
```bash
yarn build
yarn start
```

### API Documentation
Generate API documentation:
```bash
yarn docs
```

## Code Style Guidelines

### TypeScript/JavaScript

#### General Rules
- Use TypeScript for all new code
- Enable strict mode in tsconfig.json
- Use ESLint and Prettier for code formatting
- Follow functional programming principles where possible

#### Naming Conventions
```typescript
// Interfaces
interface ITokenMetadata {
  name: string;
  description: string;
  uri: string;
}

// Types
type TokenAttributes = Record<string, string | number>;

// Classes
class TokenManager {
  private readonly client: AptosClient;
}

// Constants
const MAX_BATCH_SIZE = 50;
```

#### File Organization
```typescript
// imports
import { useState, useEffect } from 'react';
import { AptosClient } from '@aptos-labs/ts-sdk';

// interfaces/types
interface Props {
  // ...
}

// component/class
export const TokenMinter: React.FC<Props> = () => {
  // ...
};
```

### Move Smart Contracts

#### General Rules
- Follow Move coding conventions
- Use descriptive names for modules and functions
- Include comprehensive test coverage
- Document public functions and modules

#### Module Structure
```move
module token::nft {
    // Imports
    use std::string;
    use aptos_framework::object;

    // Error constants
    const EINVALID_AMOUNT: u64 = 1;

    // Structs
    struct TokenMetadata has key {
        name: string::String,
        uri: string::String,
    }

    // Public functions
    public fun mint(...) {
        // Implementation
    }

    // Private helper functions
    fun validate_metadata(...) {
        // Implementation
    }
}
```

### Git Workflow

#### Branch Naming
```
feature/   # New features
bugfix/    # Bug fixes
hotfix/    # Urgent fixes
release/   # Release branches
```

#### Commit Messages
```
feat: add token minting functionality
fix: resolve transaction timeout issue
docs: update deployment instructions
test: add integration tests for marketplace
```

## Testing Guidelines

### Frontend Tests
```bash
# Run unit tests
yarn test

# Run e2e tests
yarn test:e2e

# Run coverage
yarn test:coverage
```

### Backend Tests
```bash
# Run unit tests
yarn test

# Run integration tests
yarn test:integration

# Run coverage
yarn test:coverage
```

### Contract Tests
```bash
# Run Move tests
aptos move test

# Run test coverage
aptos move coverage
```

## Deployment Process

### Testnet Deployment
1. Deploy smart contracts
```bash
cd contracts
aptos move publish --named-addresses nft_token=default
```

2. Deploy backend
```bash
cd backend
yarn build
yarn deploy:testnet
```

3. Deploy frontend
```bash
cd frontend
yarn build
yarn deploy:testnet
```

### Production Deployment (Future)
1. Security audit
2. Mainnet contract deployment
3. Production infrastructure setup
4. Monitoring configuration

## Troubleshooting

### Common Issues
1. Transaction Failures
   - Check gas settings
   - Verify account balance
   - Confirm network status

2. Compilation Errors
   - Update dependencies
   - Clear build cache
   - Check TypeScript/Move versions

3. Network Issues
   - Verify RPC endpoint
   - Check network configuration
   - Confirm wallet connection

### Support Resources
- Aptos Documentation
- Discord Community
- GitHub Issues
- Stack Overflow

## Security Guidelines

### Smart Contract Security
- Use formal verification tools
- Follow best practices for access control
- Implement emergency stops
- Regular security audits

### API Security
- Implement rate limiting
- Use proper authentication
- Validate all inputs
- Regular security scans

### Frontend Security
- Secure wallet connections
- Input validation
- XSS prevention
- Regular dependency updates
