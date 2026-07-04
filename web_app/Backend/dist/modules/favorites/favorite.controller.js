"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.FavoriteController = void 0;
const favorite_service_1 = require("./favorite.service");
class FavoriteController {
    favoriteService = new favorite_service_1.FavoriteService();
    toggleFavorite = async (req, res) => {
        try {
            const userId = BigInt(req.userId);
            const drugId = BigInt(req.body.drugId);
            const result = await this.favoriteService.toggleFavorite(userId, drugId);
            return res.json({
                success: true,
                ...result,
            });
        }
        catch (error) {
            return res.status(500).json({
                success: false,
                message: error.message,
            });
        }
    };
    getFavorites = async (req, res) => {
        try {
            const userId = BigInt(req.userId);
            const favorites = await this.favoriteService.getFavorites(userId);
            return res.json({
                success: true,
                data: favorites,
            });
        }
        catch (error) {
            return res.status(500).json({
                success: false,
                message: error.message,
            });
        }
    };
    countFavorites = async (req, res) => {
        try {
            const userId = BigInt(req.userId);
            const count = await this.favoriteService.countFavorites(userId);
            return res.json({
                success: true,
                count,
            });
        }
        catch (error) {
            return res.status(500).json({
                success: false,
                message: error.message,
            });
        }
    };
}
exports.FavoriteController = FavoriteController;
