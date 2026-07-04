import { Router } from "express";
import authController from "./auth.controller";
import { authMiddleware } from "../../middleware/auth.middleware";

const router = Router();

router.post("/register", authController.register);

router.post("/login", authController.login);

router.get(
  '/profile',
  authMiddleware,
  authController.profile
);

router.post(
  '/logout',
  authController.logout
);


export default router;
