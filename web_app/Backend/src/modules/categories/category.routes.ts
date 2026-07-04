import { Router } from "express";
import { CategoryController } from "./category.controller";

const router = Router();

const controller = new CategoryController();

router.get("/home", controller.getHomeCategories);
export default router;
