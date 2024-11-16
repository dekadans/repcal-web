import { registerSchema, validate } from "@hyperjump/json-schema/draft-2019-09";
import * as assert from "node:assert";

const HOST = process.env.REPCAL_HOST ?? 'https://repcal.info';

describe('API Tests', function () {
    describe('ApiIndex resource', function () {
        let response = null;

        before(async function(){
            response = await fetch(HOST + '/api');
        });

        it('should have 200 status code', async function () {
            assert.equal(response.status, 200);
        });
    });
});
