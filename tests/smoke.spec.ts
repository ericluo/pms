import { test, expect } from '@playwright/test';

test('登录页面可以访问', async ({ page }) => {
  const response = await page.goto('http://localhost:3001/auth/login');
  expect(response?.status()).toBe(200);
});

test('登录页面包含表单元素', async ({ page }) => {
  await page.goto('http://localhost:3001/auth/login');
  
  const emailInput = page.locator('input[type="text"]').first();
  const passwordInput = page.locator('input[type="password"]').first();
  const submitBtn = page.locator('button:has-text("登录")').first();
  
  await expect(emailInput).toBeVisible({ timeout: 10000 });
  await expect(passwordInput).toBeVisible({ timeout: 10000 });
  await expect(submitBtn).toBeVisible({ timeout: 10000 });
});

test('使用测试用户登录成功', async ({ page }) => {
  await page.goto('http://localhost:3001/auth/login');
  
  await page.fill('input[type="text"]', 'test123@example.com');
  await page.fill('input[type="password"]', '123456');
  
  const loginBtn = page.locator('button:has-text("登录")').first();
  await loginBtn.click();
  
  await page.waitForTimeout(5000);
  
  const url = page.url();
  console.log('当前URL:', url);
  
  if (url.includes('portfolio')) {
    console.log('登录成功，已跳转到投资组合页面');
  } else {
    const errorMsg = await page.locator('.el-message--error, .el-alert__title, .error-message').first().textContent().catch(() => '无错误信息');
    console.log('错误信息:', errorMsg);
  }
  
  expect(url).toContain('portfolio');
});

test('登录后可以看到导航菜单', async ({ page }) => {
  await page.goto('http://localhost:3001/auth/login');
  
  await page.fill('input[type="text"]', 'test123@example.com');
  await page.fill('input[type="password"]', '123456');
  await page.locator('button:has-text("登录")').first().click();
  
  await page.waitForTimeout(5000);
  
  const url = page.url();
  if (!url.includes('portfolio')) {
    test.skip();
  }
  
  await expect(page.locator('text=投资组合').first()).toBeVisible({ timeout: 10000 });
  await expect(page.locator('text=资产管理').first()).toBeVisible({ timeout: 10000 });
});

test('可以访问资产管理页面', async ({ page }) => {
  await page.goto('http://localhost:3001/auth/login');
  
  await page.fill('input[type="text"]', 'test123@example.com');
  await page.fill('input[type="password"]', '123456');
  await page.locator('button:has-text("登录")').first().click();
  
  await page.waitForTimeout(5000);
  
  const url = page.url();
  if (!url.includes('portfolio')) {
    test.skip();
  }
  
  await page.click('text=资产管理');
  await page.waitForTimeout(2000);
  
  expect(page.url()).toContain('/asset');
});

test('可以访问市场数据页面', async ({ page }) => {
  await page.goto('http://localhost:3001/auth/login');
  
  await page.fill('input[type="text"]', 'test123@example.com');
  await page.fill('input[type="password"]', '123456');
  await page.locator('button:has-text("登录")').first().click();
  
  await page.waitForTimeout(5000);
  
  const url = page.url();
  if (!url.includes('portfolio')) {
    test.skip();
  }
  
  await page.click('text=市场数据');
  await page.waitForTimeout(2000);
  
  expect(page.url()).toContain('/market');
});

test('可以访问业绩分析页面', async ({ page }) => {
  await page.goto('http://localhost:3001/auth/login');
  
  await page.fill('input[type="text"]', 'test123@example.com');
  await page.fill('input[type="password"]', '123456');
  await page.locator('button:has-text("登录")').first().click();
  
  await page.waitForTimeout(5000);
  
  const url = page.url();
  if (!url.includes('portfolio')) {
    test.skip();
  }
  
  await page.click('text=业绩分析');
  await page.waitForTimeout(2000);
  
  expect(page.url()).toContain('/performance');
});

test('可以访问现金管理页面', async ({ page }) => {
  await page.goto('http://localhost:3001/auth/login');
  
  await page.fill('input[type="text"]', 'test123@example.com');
  await page.fill('input[type="password"]', '123456');
  await page.locator('button:has-text("登录")').first().click();
  
  await page.waitForTimeout(5000);
  
  const url = page.url();
  if (!url.includes('portfolio')) {
    test.skip();
  }
  
  await page.click('text=现金管理');
  await page.waitForTimeout(2000);
  
  expect(page.url()).toContain('/cash');
});

test('可以访问报告页面', async ({ page }) => {
  await page.goto('http://localhost:3001/auth/login');
  
  await page.fill('input[type="text"]', 'test123@example.com');
  await page.fill('input[type="password"]', '123456');
  await page.locator('button:has-text("登录")').first().click();
  
  await page.waitForTimeout(5000);
  
  const url = page.url();
  if (!url.includes('portfolio')) {
    test.skip();
  }
  
  await page.click('text=报告');
  await page.waitForTimeout(2000);
  
  expect(page.url()).toContain('/report');
});
