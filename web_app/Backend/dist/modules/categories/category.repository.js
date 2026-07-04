"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.CategoryRepository = void 0;
const prisma_1 = __importDefault(require("../../config/prisma"));
class CategoryRepository {
    async findAll() {
        const categories = await prisma_1.default.drug_categories.findMany({
            select: {
                id: true,
                name: true,
                description: true,
                image_url: true,
            },
            orderBy: {
                name: "asc",
            },
        });
        return categories.map((category) => ({
            ...category,
            id: Number(category.id),
        }));
    }
    async findHomeCategories() {
        const [categories, total] = await prisma_1.default.$transaction([
            prisma_1.default.drug_categories.findMany({
                where: {
                    image_url: {
                        not: null,
                    },
                },
                take: 4,
                orderBy: {
                    name: "asc",
                },
                select: {
                    id: true,
                    name: true,
                    description: true,
                    image_url: true,
                },
            }),
            prisma_1.default.drug_categories.count(),
        ]);
        return {
            total,
            remaining: Math.max(total - categories.length, 0),
            categories: categories.map((category) => ({
                ...category,
                id: Number(category.id),
            })),
        };
    }
}
exports.CategoryRepository = CategoryRepository;
