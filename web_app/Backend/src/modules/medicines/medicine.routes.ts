import { Router } from "express";
import { MedicineController } from "./medicine.controller";

const router = Router();

const controller = new MedicineController();

router.get("/featured", controller.getFeaturedMedicines);

export default router;
