"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.MedicineService = void 0;
const medicine_repository_1 = require("./medicine.repository");
class MedicineService {
    medicineRepository = new medicine_repository_1.MedicineRepository();
    async getFeaturedMedicines(page) {
        return this
            .medicineRepository
            .getFeaturedMedicines(page);
    }
}
exports.MedicineService = MedicineService;
