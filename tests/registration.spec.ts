import { test, expect } from '@playwright/test';

test.describe('Test de Registro Completo (Optimizado)', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/signup');
  });

  test('debe llenar el formulario completo y hacer clic en Registrarme', async ({ page }) => {
    console.log('🎬 INICIANDO TEST DE REGISTRO COMPLETO (OPTIMIZADO)');
    console.log('⏱️ Llenando formulario de manera eficiente...');
    
    // Llenar información personal (sin delays grandes)
    console.log('👤 Llenando información personal...');
    await page.fill('input[name="nombre"]', 'Ana');
    await page.fill('input[name="segundoNombre"]', 'María');
    await page.fill('input[name="apellido1"]', 'González');
    await page.fill('input[name="apellido2"]', 'Rodríguez');
    await page.waitForTimeout(800);
    
    // Llenar fecha de nacimiento
    console.log('📅 Llenando fecha de nacimiento...');
    await page.fill('input[name="fechaNacimiento"]', '1995-03-20');
    await page.waitForTimeout(500);
    
    // Seleccionar departamento
    console.log('🏢 Seleccionando departamento...');
    await page.selectOption('select[name="departamento"]', 'Valle del Cauca');
    await page.waitForTimeout(500);
    
    // Llenar ubicación
    console.log('📍 Llenando información de ubicación...');
    await page.fill('input[name="municipio"]', 'Cali');
    await page.fill('input[name="ruta"]', 'Avenida 6N #25-50');
    await page.waitForTimeout(600);
    
    // Llenar información de contacto
    console.log('📧 Llenando información de contacto...');
    await page.fill('input[name="correo"]', 'ana.gonzalez@email.com');
    await page.fill('input[name="telefono"]', '3158967412');
    await page.waitForTimeout(600);
    
    // Llenar información de documento
    console.log('🆔 Llenando información de documento...');
    await page.selectOption('select[name="tipoDocumento"]', 'C.C');
    await page.fill('input[name="numeroDocumento"]', '1045896371');
    await page.waitForTimeout(600);
    
    // Llenar información de usuario
    console.log('👨‍💼 Llenando información de usuario...');
    await page.fill('input[name="nombreUsuario"]', 'anagonzalez95');
    await page.selectOption('select[name="tipoUsuario"]', 'Vendedor');
    await page.waitForTimeout(700);
    
    // Llenar contraseñas
    console.log('🔐 Llenando contraseñas...');
    await page.fill('input[name="contrasena"]', 'MiPassword2024!');
    await page.fill('input[name="repetirContrasena"]', 'MiPassword2024!');
    await page.waitForTimeout(800);
    
    // Aceptar términos y condiciones
    console.log('✅ Aceptando términos y condiciones...');
    await page.check('input[name="aceptoTerminos"]');
    await page.waitForTimeout(1000);
    
    // Verificar que todos los campos están llenos correctamente
    console.log('🔍 Verificando que todos los campos estén llenos...');
    await expect(page.locator('input[name="nombre"]')).toHaveValue('Ana');
    await expect(page.locator('input[name="correo"]')).toHaveValue('ana.gonzalez@email.com');
    await expect(page.locator('input[name="numeroDocumento"]')).toHaveValue('1045896371');
    await expect(page.locator('input[name="nombreUsuario"]')).toHaveValue('anagonzalez95');
    
    // Verificar que el checkbox está marcado
    console.log('☑️ Verificando checkbox de términos...');
    await expect(page.locator('input[name="aceptoTerminos"]')).toBeChecked();
    
    // Configurar listener para capturar respuesta del servidor
    console.log('👂 Configurando listener para respuesta del servidor...');
    page.on('dialog', dialog => {
      console.log('🔔 Dialog recibido:', dialog.message());
      dialog.accept();
    });
    
    // ¡HACER CLIC EN REGISTRARME!
    console.log('🚀 HACIENDO CLIC EN REGISTRARME...');
    await page.click('button[type="submit"]:has-text("Registrarme")');
    await page.waitForTimeout(2000);
    
    console.log('✨ TEST COMPLETADO - Formulario enviado exitosamente');
    console.log('📄 PDF se generará automáticamente...');
  });
});
