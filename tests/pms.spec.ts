import { test, expect } from '@playwright/test';

test.describe('PMS 前端功能测试', () => {
  test('1. 测试登录页面加载', async ({ page }) => {
    await page.goto('http://localhost:3000/auth/login');
    await page.waitForLoadState('networkidle');
    
    const title = await page.title();
    console.log('页面标题:', title);
    
    const emailInput = page.locator('input[type="text"]').first();
    const passwordInput = page.locator('input[type="password"]').first();
    const submitBtn = page.locator('button:has-text("登录")').first();
    
    await expect(emailInput).toBeVisible({ timeout: 10000 });
    await expect(passwordInput).toBeVisible({ timeout: 10000 });
    await expect(submitBtn).toBeVisible({ timeout: 10000 });
    
    console.log('登录页面元素检查通过');
  });

  test('2. 测试登录功能 - 有效凭据', async ({ page }) => {
    await page.goto('http://localhost:3000/auth/login');
    await page.waitForLoadState('networkidle');
    
    await page.fill('input[type="text"]', 'test123@example.com');
    await page.fill('input[type="password"]', '123456');
    await page.click('button:has-text("登录")');
    
    await page.waitForURL('**/portfolio', { timeout: 15000 });
    console.log('登录成功，跳转到投资组合页面');
    
    const content = await page.content();
    expect(content).toContain('投资组合');
  });

  test('3. 测试导航菜单', async ({ page }) => {
    await page.goto('http://localhost:3000/auth/login');
    await page.waitForLoadState('networkidle');
    
    await page.fill('input[type="text"]', 'test123@example.com');
    await page.fill('input[type="password"]', '123456');
    await page.click('button:has-text("登录")');
    await page.waitForURL('**/portfolio', { timeout: 15000 });
    
    const menuItems = ['投资组合', '资产管理', '业绩分析', '市场数据', '现金管理', '报告'];
    for (const item of menuItems) {
      const locator = page.locator(`text=${item}`).first();
      await expect(locator).toBeVisible({ timeout: 5000 });
      console.log(`菜单项 "${item}" 可见`);
    }
  });

  test('4. 测试资产管理页面', async ({ page }) => {
    await page.goto('http://localhost:3000/auth/login');
    await page.waitForLoadState('networkidle');
    
    await page.fill('input[type="text"]', 'test123@example.com');
    await page.fill('input[type="password"]', '123456');
    await page.click('button:has-text("登录")');
    await page.waitForURL('**/portfolio', { timeout: 15000 });
    
    await page.click('text=资产管理');
    await page.waitForTimeout(1000);
    
    const url = page.url();
    expect(url).toContain('/asset');
    console.log('资产管理页面加载成功');
  });

  test('5. 测试市场数据页面', async ({ page }) => {
    await page.goto('http://localhost:3000/auth/login');
    await page.waitForLoadState('networkidle');
    
    await page.fill('input[type="text"]', 'test123@example.com');
    await page.fill('input[type="password"]', '123456');
    await page.click('button:has-text("登录")');
    await page.waitForURL('**/portfolio', { timeout: 15000 });
    
    await page.click('text=市场数据');
    await page.waitForTimeout(1000);
    
    const url = page.url();
    expect(url).toContain('/market');
    console.log('市场数据页面加载成功');
  });

  test('6. 测试业绩分析页面', async ({ page }) => {
    await page.goto('http://localhost:3000/auth/login');
    await page.waitForLoadState('networkidle');
    
    await page.fill('input[type="text"]', 'test123@example.com');
    await page.fill('input[type="password"]', '123456');
    await page.click('button:has-text("登录")');
    await page.waitForURL('**/portfolio', { timeout: 15000 });
    
    await page.click('text=业绩分析');
    await page.waitForTimeout(1000);
    
    const url = page.url();
    expect(url).toContain('/performance');
    console.log('业绩分析页面加载成功');
  });

  test('7. 测试现金管理页面', async ({ page }) => {
    await page.goto('http://localhost:3000/auth/login');
    await page.waitForLoadState('networkidle');
    
    await page.fill('input[type="text"]', 'test123@example.com');
    await page.fill('input[type="password"]', '123456');
    await page.click('button:has-text("登录")');
    await page.waitForURL('**/portfolio', { timeout: 15000 });
    
    await page.click('text=现金管理');
    await page.waitForTimeout(1000);
    
    const url = page.url();
    expect(url).toContain('/cash');
    console.log('现金管理页面加载成功');
  });

  test('8. 测试报告页面', async ({ page }) => {
    await page.goto('http://localhost:3000/auth/login');
    await page.waitForLoadState('networkidle');
    
    await page.fill('input[type="text"]', 'test123@example.com');
    await page.fill('input[type="password"]', '123456');
    await page.click('button:has-text("登录")');
    await page.waitForURL('**/portfolio', { timeout: 15000 });
    
    await page.click('text=报告');
    await page.waitForTimeout(1000);
    
    const url = page.url();
    expect(url).toContain('/report');
    console.log('报告页面加载成功');
  });
});
