"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.MedicineRepository = void 0;
const prisma_1 = __importDefault(require("../../config/prisma"));
class MedicineRepository {
    async getFeaturedMedicines(page) {
        const skip = Math.max(page - 1, 0);
        const categories = await prisma_1.default.drug_categories.findMany({
            take: 4,
            skip: (page - 1) * 4,
            select: {
                id: true,
            },
            orderBy: {
                name: "asc",
            },
        });
        const medicines = await Promise.all(categories.map(async (category) => {
            const medicine = await prisma_1.default.drugs.findFirst({
                where: {
                    category_id: category.id,
                },
                skip,
                take: 1,
                orderBy: {
                    name: "asc",
                },
                include: {
                    drug_categories: true,
                    pharmacy_inventory: {
                        select: {
                            price: true,
                            pharmacy_id: true,
                        },
                    },
                    drug_alternatives_drug_alternatives_drug_idTodrugs: {
                        select: {
                            id: true,
                        },
                    },
                },
            });
            return medicine;
        }));
        const filtered = medicines.filter(Boolean).map((drug) => {
            const prices = drug.pharmacy_inventory
                .map((p) => Number(p.price))
                .filter((price) => !isNaN(price));
            return {
                id: Number(drug.id),
                name: drug.name,
                active_substance: drug.active_substance,
                dosage_form: drug.dosage_form,
                strength: drug.strength,
                manufacturer: drug.manufacturer,
                description: drug.description,
                image_url: drug.image_url,
                category_name: drug.drug_categories?.name,
                min_price: prices.length ? Math.min(...prices) : undefined,
                pharmacy_count: drug.pharmacy_inventory.length,
                alternatives_count: drug.drug_alternatives_drug_alternatives_drug_idTodrugs.length,
                is_available: drug.pharmacy_inventory.length > 0,
                is_favorite: false,
            };
        });
        return {
            medicines: filtered,
            hasMore: filtered.length > 0,
        };
    }
}
exports.MedicineRepository = MedicineRepository;
