import { Request, Response } from "express";

import { FavoriteService } from "./favorite.service";

export class FavoriteController {
  private favoriteService = new FavoriteService();

  toggleFavorite = async (req: Request, res: Response) => {
    try {
      const userId = BigInt(req.userId!);

      const drugId = BigInt(req.body.drugId);

      const result = await this.favoriteService.toggleFavorite(userId, drugId);

      return res.json({
        success: true,
        ...result,
      });
    } catch (error: any) {
      return res.status(500).json({
        success: false,
        message: error.message,
      });
    }
  };

  getFavorites = async (req: Request, res: Response) => {
    try {
      const userId = BigInt(req.userId!);

      const favorites = await this.favoriteService.getFavorites(userId);

      return res.json({
        success: true,
        data: favorites,
      });
    } catch (error: any) {
      return res.status(500).json({
        success: false,
        message: error.message,
      });
    }
  };

  countFavorites = async (req: Request, res: Response) => {
    try {
      const userId = BigInt(req.userId!);

      const count = await this.favoriteService.countFavorites(userId);

      return res.json({
        success: true,
        count,
      });
    } catch (error: any) {
      return res.status(500).json({
        success: false,
        message: error.message,
      });
    }
  };
}
