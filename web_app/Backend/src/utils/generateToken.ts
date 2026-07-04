import jwt, { Secret, SignOptions } from 'jsonwebtoken';

export const generateToken = (
  userId: bigint
): string => {
  const payload = {
    userId: Number(userId),
  };

  const secret: Secret = process.env.JWT_SECRET as string;

  const options: SignOptions = {
    expiresIn: '7d',
  };

  return jwt.sign(payload, secret, options);
};