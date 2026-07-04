import { Router } from "express";
import { PharmacyController } from "./pharmacy.controller";
import { authMiddleware } from "../../middleware/auth.middleware";

const router = Router();

const controller = new PharmacyController();

router.get("/", controller.getFeaturedPharmacies);

router.get("/:id", controller.getPharmacy);

router.get("/:id/medicines", controller.getPharmacyMedicines);

router.get("/:id/categories", controller.getPharmacyCategories);

router.get("/:id/reviews", controller.getPharmacyReviews);

router.post("/:id/reviews", authMiddleware, controller.addReview);

router.get("/:id/statistics", controller.getPharmacyStatistics);

export default router;
