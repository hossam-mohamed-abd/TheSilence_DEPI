import 'express';

declare global {
  namespace Express {
    interface Request {
      userId?: number;
      user: UserPayload;
    }
    interface UserPayload {
      id: number;
      email: string;
      role: string;
    }
  }
}


export {};