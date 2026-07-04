import { Request, Response } from "express";
import { CategoryService } from "./category.service";

export class CategoryController {
  private categoryService = new CategoryService();

  getHomeCategories = async (req: Request, res: Response) => {
    try {
      const result = await this.categoryService.getHomeCategories();

      return res.status(200).json({
        success: true,
        total: result.total,
        remaining: Math.max(result.total - result.categories.length, 0),
        data: result.categories,
      });
    } catch (error: any) {
      return res.status(500).json({
        success: false,
        message: error.message,
      });
    }
  };
}
