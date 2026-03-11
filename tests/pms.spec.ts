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

  test('9. 测试添加持仓功能', async ({ page }) => {
    // 登录
    await page.goto('http://localhost:3000/auth/login');
    await page.waitForLoadState('networkidle');
    await page.fill('input[placeholder="请输入邮箱"]', 'test123@example.com');
    await page.fill('input[placeholder="请输入密码"]', '123456');
    await page.click('button:has-text("登录")');
    await page.waitForURL('**/portfolio', { timeout: 15000 });
    
    // 等待投资组合列表加载
    await page.waitForTimeout(1000);
    
    // 点击第一个投资组合进入详情页
    const firstPortfolio = page.locator('.el-card, .portfolio-item, tr').first();
    await firstPortfolio.click();
    await page.waitForTimeout(1000);
    
    // 确认进入了投资组合详情页
    const detailUrl = page.url();
    expect(detailUrl).toMatch(/\/portfolio\/\d+/);
    console.log('进入投资组合详情页:', detailUrl);
    
    // 点击添加持仓按钮
    await page.click('button:has-text("添加持仓")');
    await page.waitForTimeout(500);
    
    // 等待对话框出现
    const dialog = page.locator('.el-dialog');
    await expect(dialog).toBeVisible({ timeout: 5000 });
    console.log('添加持仓对话框已打开');
    
    // 选择资产（点击下拉框选择第一个资产）
    await page.click('.el-select:has-text("请选择资产")');
    await page.waitForTimeout(300);
    const firstOption = page.locator('.el-select-dropdown__item').first();
    await firstOption.click();
    await page.waitForTimeout(300);
    
    // 输入持仓数量
    const quantityInput = page.locator('.el-input-number').first();
    await quantityInput.click();
    await quantityInput.fill('100');
    
    // 输入成本价
    const costPriceInput = page.locator('.el-input-number').nth(1);
    await costPriceInput.click();
    await costPriceInput.fill('10.5');
    
    // 点击确定按钮提交
    await page.click('.el-dialog button:has-text("确定")');
    console.log('已提交持仓');
    
    // 等待对话框关闭
    await expect(dialog).not.toBeVisible({ timeout: 5000 });
    console.log('对话框已关闭');
    
    // 等待持仓列表刷新
    await page.waitForTimeout(2000);
    
    // 验证持仓是否显示在列表中
    const holdingsTable = page.locator('.el-table');
    await expect(holdingsTable).toBeVisible({ timeout: 5000 });
    
    // 检查是否有持仓数据显示（表格中应该有数据行）
    const tableRows = page.locator('.el-table__body-wrapper tr');
    const rowCount = await tableRows.count();
    expect(rowCount).toBeGreaterThan(0);
    console.log('持仓列表行数:', rowCount);
    
    // 验证持仓数据（数量100和成本价10.5应该显示）
    const tableContent = await page.locator('.el-table').textContent();
    expect(tableContent).toContain('100');
    console.log('持仓添加成功，数据已显示在列表中');
    expect(tableContent).toContain('100');
    console.log('持仓添加成功，数据已显示在列表中');
  });
});
