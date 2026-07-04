import jwt, { Secret } from 'jsonwebtoken';

export const verifyToken = (
  token: string
) => {
  return jwt.verify(
    token,
    process.env.JWT_SECRET as Secret
  ) as {
    userId: number;
  };
};