"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.CategoryController = void 0;
const category_service_1 = require("./category.service");
class CategoryController {
    categoryService = new category_service_1.CategoryService();
    getHomeCategories = async (req, res) => {
        try {
            const result = await this.categoryService.getHomeCategories();
            return res.status(200).json({
                success: true,
                total: result.total,
                remaining: Math.max(result.total - result.categories.length, 0),
                data: result.categories,
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
exports.CategoryController = CategoryController;
