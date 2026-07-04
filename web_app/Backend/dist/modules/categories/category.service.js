"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.CategoryService = void 0;
const category_repository_1 = require("./category.repository");
class CategoryService {
    categoryRepository = new category_repository_1.CategoryRepository();
    async getHomeCategories() {
        return this.categoryRepository
            .findHomeCategories();
    }
}
exports.CategoryService = CategoryService;
