"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.FavoriteRepository = void 0;
const prisma_1 = __importDefault(require("../../config/prisma"));
class FavoriteRepository {
    async addFavorite(userId, drugId) {
        return prisma_1.default.favorites.create({
            data: {
                user_id: userId,
                drug_id: drugId,
            },
        });
    }
    async removeFavorite(userId, drugId) {
        return prisma_1.default.favorites.delete({
            where: {
                user_id_drug_id: {
                    user_id: userId,
                    drug_id: drugId,
                },
            },
        });
    }
    async findFavorite(userId, drugId) {
        return prisma_1.default.favorites.findUnique({
            where: {
                user_id_drug_id: {
                    user_id: userId,
                    drug_id: drugId,
                },
            },
        });
    }
    async getFavorites(userId) {
        const favorites = await prisma_1.default.favorites.findMany({
            where: {
                user_id: userId,
            },
            include: {
                drugs: {
                    include: {
                        drug_categories: true,
                        pharmacy_inventory: true,
                        drug_alternatives_drug_alternatives_drug_idTodrugs: true,
                    },
                },
            },
            orderBy: {
                created_at: "desc",
            },
        });
        return favorites
            .filter((f) => f.drugs)
            .map((f) => ({
            ...f.drugs,
            is_favorite: true,
            category_name: f.drugs?.drug_categories?.name,
            pharmacy_count: f.drugs?.pharmacy_inventory?.length ?? 0,
            alternatives_count: f.drugs?.drug_alternatives_drug_alternatives_drug_idTodrugs?.length ??
                0,
            min_price: f.drugs?.pharmacy_inventory?.length
                ? Math.min(...f.drugs.pharmacy_inventory.map((p) => Number(p.price)))
                : null,
            is_available: f.drugs?.pharmacy_inventory?.some((p) => (p.quantity ?? 0) > 0) ??
                false,
        }));
    }
    async countFavorites(userId) {
        return prisma_1.default.favorites.count({
            where: {
                user_id: userId,
            },
        });
    }
}
exports.FavoriteRepository = FavoriteRepository;
