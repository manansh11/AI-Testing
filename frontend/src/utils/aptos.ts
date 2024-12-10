import { Aptos, AptosConfig, Network } from '@aptos-labs/ts-sdk';

const config = new AptosConfig({
  network: Network.TESTNET,
  fullnode: process.env.APTOS_NODE_URL,
  faucet: process.env.APTOS_FAUCET_URL
});

export const aptosClient = new Aptos(config);

export const testConnection = async (): Promise<boolean> => {
  try {
    await aptosClient.getLedgerInfo();
    return true;
  } catch (error) {
    console.error('Failed to connect to Aptos network:', error);
    return false;
  }
};
