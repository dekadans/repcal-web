import { registerSchema, validate } from "@hyperjump/json-schema/draft-2019-09";
import { strict as assert } from 'node:assert';

const HOST = process.env.REPCAL_HOST ?? 'https://repcal.info';

async function schemaValidate(resource) {
    const schemaUri = resource._links.describedby.href;
    const result = await validate(schemaUri, resource);
    return result.valid;
}

describe('API Tests', function () {
    describe('ApiIndex resource', function () {
        let response, resource;

        before(async function(){
            response = await fetch(HOST + '/api');
            resource = await response.json();
        });

        it('should have 200 status code',  function () {
            assert.equal(response.status, 200);
        });

        it('should have HAL content-type',  function () {
            assert.equal(response.headers.get('content-type'), 'application/hal+json');
        });

        it('should validate against schema',  async function () {
            assert.equal(await schemaValidate(resource), true);
        });
    });

    describe('Now operation', function () {
        let response, resource;

        before(async function(){
            response = await fetch(HOST + '/now?offset=60');
            resource = await response.json();
        });

        it('should have 200 status code',  function () {
            assert.equal(response.status, 200);
        });

        it('should have been redirected',  function () {
            assert.equal(response.redirected, true);
        });

        it('should have HAL content-type',  function () {
            assert.equal(response.headers.get('content-type'), 'application/hal+json');
        });

        it('should have reasonable self link', function() {
            const self = resource._links.self.href;
            assert.equal(self.includes('moment'), true);
            assert.equal(self.endsWith('/60'), true);
        });
    });

    describe('Moment resource', function () {
        describe('Valid', function () {
            const uri = '/moment/1731849489/0';
            let response, resource;

            before(async function(){
                response = await fetch(HOST + uri);
                resource = await response.json();
            });

            it('should have 200 status code',  function () {
                assert.equal(response.status, 200);
            });

            it('should have HAL content-type',  function () {
                assert.equal(response.headers.get('content-type'), 'application/hal+json');
            });

            it('should have reasonable self link', function() {
                assert.equal(
                    resource._links.self.href.includes(uri),
                    true
                );
            });

            it('should validate against schema',  async function () {
                assert.equal(await schemaValidate(resource), true);
            });
        });

        describe('Invalid', function () {
            let response;

            before(async function(){
                response = await fetch(HOST + '/moment/what/nope');
            });

            it('should have 404 status code',  function () {
                assert.equal(response.status, 404);
            });

            it('should have Problem Details content-type',  function () {
                assert.equal(response.headers.get('content-type'), 'application/problem+json');
            });
        });
    });

    describe('Date resource', function () {
        describe('Valid', function () {
            const uri = '/date/2024/11/15';
            let response, resource;

            before(async function(){
                response = await fetch(HOST + uri);
                resource = await response.json();
            });

            it('should have 200 status code',  function () {
                assert.equal(response.status, 200);
            });

            it('should have HAL content-type',  function () {
                assert.equal(response.headers.get('content-type'), 'application/hal+json');
            });

            it('should have reasonable self link', function() {
                assert.equal(
                    resource._links.self.href.includes(uri),
                    true
                );
            });

            it('should validate against schema',  async function () {
                assert.equal(await schemaValidate(resource), true);
            });
        });

        describe('Invalid', function () {
            let response;

            before(async function(){
                response = await fetch(HOST + '/date/100/100/100');
            });

            it('should have 404 status code',  function () {
                assert.equal(response.status, 404);
            });

            it('should have Problem Details content-type',  function () {
                assert.equal(response.headers.get('content-type'), 'application/problem+json');
            });
        });
    });

    describe('Time resource', function () {
        describe('Valid', function () {
            const uri = '/time/14/21/30';
            let response, resource;

            before(async function(){
                response = await fetch(HOST + uri);
                resource = await response.json();
            });

            it('should have 200 status code',  function () {
                assert.equal(response.status, 200);
            });

            it('should have HAL content-type',  function () {
                assert.equal(response.headers.get('content-type'), 'application/hal+json');
            });

            it('should have reasonable self link', function() {
                assert.equal(
                    resource._links.self.href.includes(uri),
                    true
                );
            });

            it('should validate against schema',  async function () {
                assert.equal(await schemaValidate(resource), true);
            });
        });

        describe('Invalid', function () {
            let response;

            before(async function(){
                response = await fetch(HOST + '/time/81/72/63');
            });

            it('should have 404 status code',  function () {
                assert.equal(response.status, 404);
            });

            it('should have Problem Details content-type',  function () {
                assert.equal(response.headers.get('content-type'), 'application/problem+json');
            });
        });
    });

    describe('Observance resource', function () {
        describe('Valid', function () {
            const uri = '/observance/57';
            let response, resource;

            before(async function(){
                response = await fetch(HOST + uri);
                resource = await response.json();
            });

            it('should have 200 status code',  function () {
                assert.equal(response.status, 200);
            });

            it('should have HAL content-type',  function () {
                assert.equal(response.headers.get('content-type'), 'application/hal+json');
            });

            it('should have reasonable self link', function() {
                assert.equal(
                    resource._links.self.href.includes(uri),
                    true
                );
            });

            it('should validate against schema',  async function () {
                assert.equal(await schemaValidate(resource), true);
            });
        });

        describe('Invalid', function () {
            let response;

            before(async function(){
                response = await fetch(HOST + '/observance/what');
            });

            it('should have 404 status code',  function () {
                assert.equal(response.status, 404);
            });

            it('should have Problem Details content-type',  function () {
                assert.equal(response.headers.get('content-type'), 'application/problem+json');
            });
        });
    });

    describe('API documentation', function () {
        let response;

        before(async function(){
            response = await fetch(HOST + '/meta/service/doc');
        });

        it('should have 200 status code',  function () {
            assert.equal(response.status, 200);
        });

        it('should have Markdown content-type',  function () {
            assert.equal(response.headers.get('content-type').includes('text/markdown'), true);
        });
    });

    describe('Observance transform', function () {
        let response;

        before(async function(){
            response = await fetch(HOST + '/meta/transform/observance');
        });

        it('should have 200 status code',  function () {
            assert.equal(response.status, 200);
        });

        it('should have XML content-type',  function () {
            assert.equal(response.headers.get('content-type').includes('application/xml'), true);
        });
    });
});
