"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.PharmacyRepository = void 0;
const prisma_1 = __importDefault(require("../../config/prisma"));
class PharmacyRepository {
    async getFeaturedPharmacies(page, limit = 4) {
        const skip = (page - 1) * limit;
        const pharmacies = await prisma_1.default.pharmacies.findMany({
            where: {
                is_active: true,
            },
            include: {
                cities: true,
                pharmacy_inventory: true,
                pharmacy_ratings: true,
            },
            orderBy: {
                created_at: "desc",
            },
            skip,
            take: limit,
        });
        return pharmacies.map((p) => {
            const ratings = p.pharmacy_ratings.map((r) => r.rating ?? 0);
            const avgRating = ratings.length
                ? ratings.reduce((a, b) => a + b, 0) / ratings.length
                : 0;
            return {
                id: p.id,
                name: p.name,
                logo_url: p.logo_url,
                address: p.address,
                city_name: p.cities?.name,
                medicines_count: p.pharmacy_inventory.length,
                reviews_count: p.pharmacy_ratings.length,
                avg_rating: Number(avgRating.toFixed(1)),
            };
        });
    }
    async findById(id) {
        return prisma_1.default.pharmacies.findUnique({
            where: {
                id,
            },
            include: {
                cities: {
                    include: {
                        governorates: true,
                    },
                },
                pharmacy_inventory: {
                    select: {
                        quantity: true,
                        drug_id: true,
                        drugs: {
                            select: {
                                category_id: true,
                            },
                        },
                    },
                },
                pharmacy_ratings: {
                    select: {
                        rating: true,
                    },
                },
            },
        });
    }
    async findMedicines(pharmacyId, options) {
        const page = options.page || 1;
        const limit = options.limit || 12;
        const skip = (page - 1) * limit;
        const where = {
            pharmacy_id: pharmacyId,
        };
        if (options.available) {
            where.quantity = {
                gt: 0,
            };
        }
        if (options.search) {
            where.drugs = {
                name: {
                    contains: options.search,
                    mode: "insensitive",
                },
            };
        }
        if (options.category) {
            where.drugs = {
                ...where.drugs,
                category_id: options.category,
            };
        }
        const total = await prisma_1.default.pharmacy_inventory.count({
            where,
        });
        const data = await prisma_1.default.pharmacy_inventory.findMany({
            where,
            skip,
            take: limit,
            include: {
                drugs: {
                    include: {
                        drug_categories: true,
                        drug_alternatives_drug_alternatives_drug_idTodrugs: true,
                    },
                },
            },
        });
        const medicines = data.map((item) => ({
            id: Number(item.drugs.id),
            name: item.drugs?.name,
            active_substance: item.drugs?.active_substance,
            dosage_form: item.drugs?.dosage_form,
            strength: item.drugs?.strength,
            manufacturer: item.drugs?.manufacturer,
            description: item.drugs?.description,
            image_url: item.drugs?.image_url,
            category_name: item.drugs?.drug_categories?.name,
            min_price: Number(item.price),
            pharmacy_count: 1,
            alternatives_count: item.drugs?.drug_alternatives_drug_alternatives_drug_idTodrugs
                ?.length ?? 0,
            is_available: (item.quantity ?? 0) > 0,
            is_favorite: false,
        }));
        return {
            page,
            limit,
            total,
            hasMore: skip + limit < total,
            data: medicines,
        };
    }
    async findCategories(pharmacyId) {
        const inventory = await prisma_1.default.pharmacy_inventory.findMany({
            where: {
                pharmacy_id: pharmacyId,
            },
            include: {
                drugs: {
                    include: {
                        drug_categories: true,
                    },
                },
            },
        });
        const map = new Map();
        inventory.forEach((item) => {
            const cat = item.drugs?.drug_categories;
            if (!cat)
                return;
            const id = Number(cat.id);
            if (!map.has(id)) {
                map.set(id, {
                    id,
                    name: cat.name,
                    count: 1,
                });
            }
            else {
                map.get(id).count++;
            }
        });
        return [...map.values()];
    }
    async findReviews(pharmacyId, page) {
        const take = 5;
        const skip = (page - 1) * take;
        const total = await prisma_1.default.pharmacy_ratings.count({
            where: {
                pharmacy_id: pharmacyId,
            },
        });
        const data = await prisma_1.default.pharmacy_ratings.findMany({
            where: {
                pharmacy_id: pharmacyId,
            },
            skip,
            take,
            include: {
                users: {
                    select: {
                        id: true,
                        first_name: true,
                        last_name: true,
                        profile_image: true,
                    },
                },
            },
            orderBy: {
                created_at: "desc",
            },
        });
        return {
            total,
            page,
            hasMore: skip + take < total,
            data,
        };
    }
    async createReview(pharmacyId, userId, rating, review) {
        return prisma_1.default.pharmacy_ratings.upsert({
            where: {
                user_id_pharmacy_id: {
                    user_id: userId,
                    pharmacy_id: pharmacyId,
                },
            },
            update: {
                rating,
                review,
            },
            create: {
                pharmacy_id: pharmacyId,
                user_id: userId,
                rating,
                review,
                created_at: new Date(),
            },
        });
    }
    async getStatistics(pharmacyId) {
        const inventory = await prisma_1.default.pharmacy_inventory.findMany({
            where: {
                pharmacy_id: pharmacyId,
            },
            include: {
                drugs: true,
            },
        });
        const categories = new Set(inventory.map((i) => i.drugs?.category_id));
        const available = inventory.filter((i) => (i.quantity ?? 0) > 0).length;
        const avgPrice = inventory.length
            ? inventory.reduce((a, b) => a + Number(b.price ?? 0), 0) /
                inventory.length
            : 0;
        return {
            medicines_count: inventory.length,
            available_count: available,
            categories_count: categories.size,
            average_price: Number(avgPrice.toFixed(2)),
        };
    }
}
exports.PharmacyRepository = PharmacyRepository;
