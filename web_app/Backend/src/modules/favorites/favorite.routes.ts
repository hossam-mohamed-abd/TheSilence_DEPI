import { Router } from "express";

import { FavoriteController } from "./favorite.controller";

import { authMiddleware } from "../../middleware/auth.middleware";



const router = Router();

const controller = new FavoriteController();

router.use(authMiddleware);

router.post("/", controller.toggleFavorite);

router.get("/", controller.getFavorites);

router.get("/count", controller.countFavorites);

export default router;
