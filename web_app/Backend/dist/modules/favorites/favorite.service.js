"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.FavoriteService = void 0;
const favorite_repository_1 = require("./favorite.repository");
class FavoriteService {
    favoriteRepository = new favorite_repository_1.FavoriteRepository();
    async toggleFavorite(userId, drugId) {
        const favorite = await this.favoriteRepository
            .findFavorite(userId, drugId);
        if (favorite) {
            await this.favoriteRepository
                .removeFavorite(userId, drugId);
            return {
                isFavorite: false,
            };
        }
        await this.favoriteRepository
            .addFavorite(userId, drugId);
        return {
            isFavorite: true,
        };
    }
    async getFavorites(userId) {
        return this.favoriteRepository
            .getFavorites(userId);
    }
    async countFavorites(userId) {
        return this.favoriteRepository
            .countFavorites(userId);
    }
}
exports.FavoriteService = FavoriteService;
