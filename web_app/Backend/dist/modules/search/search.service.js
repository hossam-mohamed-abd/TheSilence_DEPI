"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.SearchService = void 0;
const search_repository_1 = require("./search.repository");
class SearchService {
    repository = new search_repository_1.SearchRepository();
    async search(q, page, limit) {
        return this.repository.search(q, page, limit);
    }
}
exports.SearchService = SearchService;
