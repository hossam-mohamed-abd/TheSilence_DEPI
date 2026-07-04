"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.StatisticsRepository = void 0;
const prisma_1 = __importDefault(require("../../config/prisma"));
class StatisticsRepository {
    async getStatistics() {
        const [medicinesCount, pharmaciesCount,] = await Promise.all([
            prisma_1.default.drugs.count(),
            prisma_1.default.pharmacies.count({
                where: {
                    is_active: true,
                },
            }),
        ]);
        return {
            medicinesCount,
            pharmaciesCount,
        };
    }
}
exports.StatisticsRepository = StatisticsRepository;
