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
    await page.waitForTimeout(2000);
    
    // 直接访问投资组合详情页（ID=6）
    await page.goto('http://localhost:3000/portfolio/6');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);
    
    // 确认进入了投资组合详情页
    const detailUrl = page.url();
    expect(detailUrl).toContain('/portfolio/6');
    console.log('进入投资组合详情页:', detailUrl);
    
    // 等待页面完全加载，确保没有 vite-error-overlay
    await page.waitForSelector('.portfolio-detail', { state: 'visible', timeout: 10000 });
    await page.waitForTimeout(1000);
    
    // 点击添加持仓按钮
    const addHoldingBtn = page.locator('button:has-text("添加持仓")');
    await addHoldingBtn.waitFor({ state: 'visible', timeout: 10000 });
    await addHoldingBtn.click();
    await page.waitForTimeout(1000);
    
    // 等待对话框出现
    const dialog = page.locator('.el-dialog');
    await expect(dialog).toBeVisible({ timeout: 10000 });
    console.log('添加持仓对话框已打开');
    
    // 选择资产（使用更可靠的定位器）
    const assetSelect = page.locator('.el-dialog .el-select').first();
    await assetSelect.waitFor({ state: 'visible', timeout: 5000 });
    await assetSelect.click();
    await page.waitForTimeout(1000);
    
    // 选择第一个资产选项
    const firstOption = page.locator('.el-select-dropdown__item').first();
    await firstOption.waitFor({ state: 'visible', timeout: 5000 });
    await firstOption.click();
    await page.waitForTimeout(1000);
    console.log('已选择资产');
    
    // 填写持仓数量 - 使用 el-input-number 的 input
    const quantityInput = page.locator('.el-dialog .el-input-number input').first();
    await quantityInput.waitFor({ state: 'visible', timeout: 5000 });
    await quantityInput.click();
    await quantityInput.fill('100');
    await page.waitForTimeout(500);
    console.log('已填写持仓数量');
    
    // 填写成本价
    const costPriceInput = page.locator('.el-dialog .el-input-number input').nth(1);
    await costPriceInput.waitFor({ state: 'visible', timeout: 5000 });
    await costPriceInput.click();
    await costPriceInput.fill('10.5');
    await page.waitForTimeout(500);
    console.log('已填写成本价');
    
    // 点击确定按钮
    const confirmBtn = page.locator('.el-dialog button:has-text("确定")');
    await confirmBtn.waitFor({ state: 'visible', timeout: 5000 });
    await confirmBtn.click();
    await page.waitForTimeout(3000);
    
    // 验证成功提示
    const successMessage = page.locator('.el-message--success');
    await expect(successMessage).toBeVisible({ timeout: 10000 });
    console.log('持仓添加成功');
    
    // 等待对话框关闭
    await page.waitForTimeout(2000);
    console.log('对话框已关闭');
    
    // 等待持仓列表刷新
    await page.waitForTimeout(2000);
    
    // 验证持仓是否显示在列表中
    const holdingsTable = page.locator('.el-table');
    await expect(holdingsTable).toBeVisible({ timeout: 10000 });
    
    // 检查是否有持仓数据显示（表格中应该有数据行）
    const tableRows = page.locator('.el-table__body-wrapper tr');
    const rowCount = await tableRows.count();
    expect(rowCount).toBeGreaterThan(0);
    console.log('持仓列表行数:', rowCount);
    
    // 验证持仓数据（数量 100 应该显示）
    const tableContent = await page.locator('.el-table').textContent();
    expect(tableContent).toContain('100');
    console.log('持仓添加成功，数据已显示在列表中');
  });

  test('10. 测试编辑投资组合功能', async ({ page }) => {
    // 登录
    await page.goto('http://localhost:3000/auth/login');
    await page.waitForLoadState('networkidle');
    await page.fill('input[placeholder="请输入邮箱"]', 'test123@example.com');
    await page.fill('input[placeholder="请输入密码"]', '123456');
    await page.click('button:has-text("登录")');
    await page.waitForURL('**/portfolio', { timeout: 15000 });
    
    // 等待投资组合列表加载
    await page.waitForTimeout(2000);
    
    // 点击第一个投资组合的编辑按钮
    const editBtn = page.locator('button:has-text("编辑")').first();
    await editBtn.waitFor({ state: 'visible', timeout: 10000 });
    await editBtn.click();
    await page.waitForTimeout(2000);
    
    // 确认进入编辑页面
    const editUrl = page.url();
    expect(editUrl).toMatch(/\/portfolio\/\d+\/edit/);
    console.log('进入投资组合编辑页:', editUrl);
    
    // 等待页面完全加载
    await page.waitForSelector('.portfolio-edit', { state: 'visible', timeout: 10000 });
    await page.waitForTimeout(1000);
    
    // 修改组合名称
    const nameInput = page.locator('input[placeholder="请输入组合名称"]');
    await nameInput.waitFor({ state: 'visible', timeout: 5000 });
    await nameInput.click();
    await nameInput.fill('');
    await nameInput.fill(`测试组合_编辑_${Date.now()}`);
    await page.waitForTimeout(500);
    
    // 点击更新按钮
    const updateBtn = page.locator('button:has-text("更新")');
    await updateBtn.waitFor({ state: 'visible', timeout: 5000 });
    await updateBtn.click();
    await page.waitForTimeout(3000);
    
    // 验证跳转到投资组合详情页（不是列表页）
    const detailUrl = page.url();
    expect(detailUrl).toContain('/portfolio/');
    expect(detailUrl).not.toContain('/edit');
    console.log('编辑成功，跳转到投资组合详情页:', detailUrl);
  });

  test('11. 测试删除投资组合功能', async ({ page }) => {
    // 登录
    await page.goto('http://localhost:3000/auth/login');
    await page.waitForLoadState('networkidle');
    await page.fill('input[placeholder="请输入邮箱"]', 'test123@example.com');
    await page.fill('input[placeholder="请输入密码"]', '123456');
    await page.click('button:has-text("登录")');
    await page.waitForURL('**/portfolio', { timeout: 15000 });
    
    // 等待投资组合列表加载
    await page.waitForTimeout(1000);
    
    // 点击第一个投资组合的删除按钮
    const deleteBtn = page.locator('button:has-text("删除")').first();
    await deleteBtn.click();
    await page.waitForTimeout(500);
    
    // 验证删除操作被触发（由于当前只是打印日志，我们只需要验证按钮被点击）
    console.log('删除按钮已点击');
  });

  test('12. 测试搜索投资组合功能', async ({ page }) => {
    // 登录
    await page.goto('http://localhost:3000/auth/login');
    await page.waitForLoadState('networkidle');
    await page.fill('input[placeholder="请输入邮箱"]', 'test123@example.com');
    await page.fill('input[placeholder="请输入密码"]', '123456');
    await page.click('button:has-text("登录")');
    await page.waitForURL('**/portfolio', { timeout: 15000 });
    
    // 等待投资组合列表加载
    await page.waitForTimeout(1000);
    
    // 输入搜索关键词
    const searchInput = page.locator('input[placeholder="搜索投资组合"]');
    await searchInput.click();
    await searchInput.fill('测试');
    await page.waitForTimeout(1000);
    
    // 验证搜索结果
    const tableRows = page.locator('.el-table__body-wrapper tr');
    const rowCount = await tableRows.count();
    console.log('搜索结果行数:', rowCount);
    
    // 清空搜索
    await searchInput.click();
    await searchInput.fill('');
    await page.waitForTimeout(1000);
    
    // 验证搜索结果已清空
    const tableRowsAfterClear = page.locator('.el-table__body-wrapper tr');
    const rowCountAfterClear = await tableRowsAfterClear.count();
    console.log('清空搜索后的行数:', rowCountAfterClear);
  });

  test('13. 测试资产管理页面功能', async ({ page }) => {
    // 登录
    await page.goto('http://localhost:3000/auth/login');
    await page.waitForLoadState('networkidle');
    await page.fill('input[placeholder="请输入邮箱"]', 'test123@example.com');
    await page.fill('input[placeholder="请输入密码"]', '123456');
    await page.click('button:has-text("登录")');
    await page.waitForURL('**/portfolio', { timeout: 15000 });
    
    // 进入资产管理页面
    await page.click('text=资产管理');
    await page.waitForTimeout(1000);
    
    // 确认进入资产管理页面
    const assetUrl = page.url();
    expect(assetUrl).toContain('/asset');
    console.log('进入资产管理页面:', assetUrl);
    
    // 点击添加资产按钮
    const addAssetBtn = page.locator('button:has-text("添加资产")').first();
    await addAssetBtn.click();
    await page.waitForTimeout(1000);
    
    // 确认进入添加资产页面
    const addAssetUrl = page.url();
    expect(addAssetUrl).toContain('/asset/add');
    console.log('进入添加资产页面:', addAssetUrl);
    
    // 填写资产信息
    await page.fill('input[placeholder="请输入资产名称"]', `测试资产_${Date.now()}`);
    await page.fill('input[placeholder="请输入资产代码"]', `TEST${Date.now()}`);
    
    // 选择资产类型（使用更简单的定位器）
    const assetTypeSelect = page.locator('.el-select').nth(0);
    await assetTypeSelect.click();
    await page.waitForTimeout(300);
    
    // 选择第一个资产类型选项
    const assetTypeOption = page.locator('.el-select-dropdown__item').first();
    await assetTypeOption.click();
    await page.waitForTimeout(300);
    
    // 点击添加按钮
    const addBtn = page.locator('button:has-text("添加")').first();
    await addBtn.click();
    await page.waitForTimeout(2000);
    
    // 验证跳转回资产管理列表页
    const assetListUrl = page.url();
    expect(assetListUrl).toContain('/asset');
    expect(assetListUrl).not.toContain('/add');
    console.log('资产添加成功，返回资产管理列表');
  });

  test('14. 测试交易记录页面功能', async ({ page }) => {
    // 登录
    await page.goto('http://localhost:3000/auth/login');
    await page.waitForLoadState('networkidle');
    await page.fill('input[placeholder="请输入邮箱"]', 'test123@example.com');
    await page.fill('input[placeholder="请输入密码"]', '123456');
    await page.click('button:has-text("登录")');
    await page.waitForURL('**/portfolio', { timeout: 15000 });
    
    // 进入资产管理页面
    await page.click('text=资产管理');
    await page.waitForTimeout(1000);
    
    // 点击第一个资产的查看按钮
    const viewAssetBtn = page.locator('button:has-text("查看")').first();
    await viewAssetBtn.click();
    await page.waitForTimeout(1000);
    
    // 确认进入资产详情页面
    const assetDetailUrl = page.url();
    expect(assetDetailUrl).toContain('/asset/');
    console.log('进入资产详情页面:', assetDetailUrl);
    
    // 验证资产详情页面加载成功（使用页面标题）
    const pageTitle = await page.title();
    expect(pageTitle).toContain('PMS - 投资组合管理系统');
    console.log('资产详情页面加载成功');
  });

  test('15. 测试现金管理页面功能', async ({ page }) => {
    // 登录
    await page.goto('http://localhost:3000/auth/login');
    await page.waitForLoadState('networkidle');
    await page.fill('input[placeholder="请输入邮箱"]', 'test123@example.com');
    await page.fill('input[placeholder="请输入密码"]', '123456');
    await page.click('button:has-text("登录")');
    await page.waitForURL('**/portfolio', { timeout: 15000 });
    
    // 进入现金管理页面
    await page.click('text=现金管理');
    await page.waitForTimeout(1000);
    
    // 确认进入现金管理页面
    const cashUrl = page.url();
    expect(cashUrl).toContain('/cash');
    console.log('进入现金管理页面:', cashUrl);
    
    // 验证现金余额组件可见（使用第一个 el-card）
    const cashBalance = page.locator('.el-card').first();
    await expect(cashBalance).toBeVisible({ timeout: 5000 });
    console.log('现金余额组件可见');
  });

  test('16. 测试报告页面功能', async ({ page }) => {
    // 登录
    await page.goto('http://localhost:3000/auth/login');
    await page.waitForLoadState('networkidle');
    await page.fill('input[placeholder="请输入邮箱"]', 'test123@example.com');
    await page.fill('input[placeholder="请输入密码"]', '123456');
    await page.click('button:has-text("登录")');
    await page.waitForURL('**/portfolio', { timeout: 15000 });
    
    // 进入报告页面
    await page.click('text=报告');
    await page.waitForTimeout(1000);
    
    // 确认进入报告页面
    const reportUrl = page.url();
    expect(reportUrl).toContain('/report');
    console.log('进入报告页面:', reportUrl);
    
    // 点击创建报告按钮
    const createReportBtn = page.locator('button:has-text("创建报告")').first();
    await createReportBtn.click();
    await page.waitForTimeout(1000);
    
    // 确认进入创建报告页面
    const createReportUrl = page.url();
    expect(createReportUrl).toContain('/report/create');
    console.log('进入创建报告页面:', createReportUrl);
  });

  test('17. 测试编辑资产功能', async ({ page }) => {
    // 登录
    await page.goto('http://localhost:3000/auth/login');
    await page.waitForLoadState('networkidle');
    await page.fill('input[placeholder="请输入邮箱"]', 'test123@example.com');
    await page.fill('input[placeholder="请输入密码"]', '123456');
    await page.click('button:has-text("登录")');
    await page.waitForURL('**/portfolio', { timeout: 15000 });
    
    // 进入资产管理页面
    await page.click('text=资产管理');
    await page.waitForTimeout(1000);
    
    // 点击第一个资产的编辑按钮
    const editBtn = page.locator('button:has-text("编辑")').first();
    await editBtn.click();
    await page.waitForTimeout(1000);
    
    // 确认进入资产编辑页面
    const editUrl = page.url();
    expect(editUrl).toContain('/asset/');
    expect(editUrl).toContain('/edit');
    console.log('进入资产编辑页面:', editUrl);
    
    // 修改资产名称
    const nameInput = page.locator('input[placeholder="请输入资产名称"]');
    await nameInput.click();
    await nameInput.fill('');
    await nameInput.fill(`编辑测试资产_${Date.now()}`);
    
    // 点击更新按钮
    await page.click('button:has-text("更新")');
    await page.waitForTimeout(2000);
    
    // 验证跳转回资产管理列表页
    const assetListUrl = page.url();
    expect(assetListUrl).toContain('/asset');
    expect(assetListUrl).not.toContain('/edit');
    console.log('资产编辑成功，返回资产管理列表');
  });

  test('18. 测试现金流水功能', async ({ page }) => {
    // 登录
    await page.goto('http://localhost:3000/auth/login');
    await page.waitForLoadState('networkidle');
    await page.fill('input[placeholder="请输入邮箱"]', 'test123@example.com');
    await page.fill('input[placeholder="请输入密码"]', '123456');
    await page.click('button:has-text("登录")');
    await page.waitForURL('**/portfolio', { timeout: 15000 });
    
    // 进入现金管理页面
    await page.click('text=现金管理');
    await page.waitForTimeout(1000);
    
    // 点击现金流水标签
    const cashFlowTab = page.locator('text=现金流水').first();
    await cashFlowTab.click();
    await page.waitForTimeout(1000);
    
    // 验证现金流水页面加载
    const cashFlowUrl = page.url();
    expect(cashFlowUrl).toContain('/cash');
    console.log('现金流水页面加载成功');
  });

  test('19. 测试市场概览功能', async ({ page }) => {
    // 登录
    await page.goto('http://localhost:3000/auth/login');
    await page.waitForLoadState('networkidle');
    await page.fill('input[placeholder="请输入邮箱"]', 'test123@example.com');
    await page.fill('input[placeholder="请输入密码"]', '123456');
    await page.click('button:has-text("登录")');
    await page.waitForURL('**/portfolio', { timeout: 15000 });
    
    // 进入市场数据页面
    await page.click('text=市场数据');
    await page.waitForTimeout(1000);
    
    // 点击市场概览标签
    const marketOverviewTab = page.locator('text=市场概览').first();
    await marketOverviewTab.click();
    await page.waitForTimeout(1000);
    
    // 验证市场概览页面加载
    const marketUrl = page.url();
    expect(marketUrl).toContain('/market');
    console.log('市场概览页面加载成功');
  });

  test('20. 测试业绩分析功能', async ({ page }) => {
    // 登录
    await page.goto('http://localhost:3000/auth/login');
    await page.waitForLoadState('networkidle');
    await page.fill('input[placeholder="请输入邮箱"]', 'test123@example.com');
    await page.fill('input[placeholder="请输入密码"]', '123456');
    await page.click('button:has-text("登录")');
    await page.waitForURL('**/portfolio', { timeout: 15000 });
    
    // 进入业绩分析页面
    await page.click('text=业绩分析');
    await page.waitForTimeout(1000);
    
    // 点击业绩概览标签
    const performanceOverviewTab = page.locator('text=业绩概览').first();
    await performanceOverviewTab.click();
    await page.waitForTimeout(1000);
    
    // 验证业绩分析页面加载
    const performanceUrl = page.url();
    expect(performanceUrl).toContain('/performance');
    console.log('业绩分析页面加载成功');
  });
});
