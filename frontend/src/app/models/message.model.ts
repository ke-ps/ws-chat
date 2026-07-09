export interface Message {
  id: string;
  content: string;
  sender: string;
  senderType: 'USER' | 'AI' | 'SYSTEM';
  timestamp: Date;
}