import { Request, Response } from "express";
import authService from "./auth.service";
import { serializeBigInt } from "../../utils/bigintSerializer";

class AuthController {
  async register(req: Request, res: Response) {
    console.log(req.body);

    try {
      const result = await authService.register(req.body);

      res.cookie("token", result.token, {
        httpOnly: true,
        secure: process.env.NODE_ENV === "production",
        sameSite: "lax",
        maxAge: 7 * 24 * 60 * 60 * 1000,
      });

      res.status(201).json({
        success: true,
        user: serializeBigInt(result.user),
      });
    } catch (error: any) {
      res.status(400).json({
        success: false,
        message: error.message,
      });
    }
  }

  async login(req: Request, res: Response) {
    try {
      const result = await authService.login(req.body);

      const isProduction = process.env.NODE_ENV === "production";

      res.cookie("token", result.token, {
        httpOnly: true,
        secure: isProduction,
        sameSite: isProduction ? "none" : "lax",
        maxAge: 7 * 24 * 60 * 60 * 1000,
      });
      res.status(200).json(
        serializeBigInt({
          success: true,
          user: result.user,
        }),
      );
    } catch (error: any) {
      res.status(400).json({
        success: false,
        message: error.message,
      });
    }
  }

  async profile(req: Request, res: Response) {
    try {
      const user = await authService.profile(req.userId!);

      res.json(
        serializeBigInt({
          success: true,
          user,
        }),
      );
    } catch (error: any) {
      res.status(404).json({
        success: false,
        message: error.message,
      });
    }
  }

  async logout(req: Request, res: Response) {
    const isProduction = process.env.NODE_ENV === "production";

    res.clearCookie("token", {
      httpOnly: true,
      secure: isProduction,
      sameSite: isProduction ? "none" : "lax",
    });

    res.status(200).json({
      success: true,
      message: "Logged out successfully",
    });
  }
}

export default new AuthController();
