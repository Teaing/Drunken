  public Map<String, Object> certFileUpload()
  {
    Map<String, Object> retMap = new HashMap();
    FileDialog fd = new FileDialog(SystemInit.getSfuShell());
    fd.setFilterExtensions(new String[] { "*.key" });
    fd.setText("S1离线证书导入");
    String saveFile = fd.open();
    if (saveFile != null)
    {
      LOG.info("Install path:" + new File(SystemUtil.CERT_FILE_PATH).getAbsolutePath());
      File oldCertFile = new File(SystemUtil.CERT_FILE_PATH);
      File newCertFile = new File(saveFile);
      File tmpFile = new File(SystemUtil.CERT_FILE_PATH + newCertFile.getName() + ".dat");
      try
      {
        int fileKey = 428343592;  // 异或的值
        FileUtils.copyFileToDirectory(newCertFile, oldCertFile);
        int seekFile = 0;
        InputStream fis = new FileInputStream(newCertFile); //  文件流方式读取文件
        FileOutputStream fos = new FileOutputStream(tmpFile); // 文件流方式输出文件
        while ((seekFile = fis.read()) > -1) {  //  读取数据的每一位
          fos.write(seekFile ^ fileKey);  //  异或，其实跟 428343592 % 256 的值一样，跟40异或
        }
        InputStream tf = new FileInputStream(tmpFile);  
        BufferedReader in = new BufferedReader(new InputStreamReader(tf));
        StringBuffer buffer = new StringBuffer();
        String line = "";
        while ((line = in.readLine()) != null) {
          buffer.append(line);
        }
        String userInfo = EncryptUtil.decryptBy3DES(buffer.toString(), "我是很长的密钥"); // 异或过的文件再读进来进行解密，所以加密方式是3DES加密后再异或保存为加密后的文件
        LOG.info("Info:" + userInfo);
        ParserConfig jcParserConfig = new ParserConfig();
        ......
        ......
        ......
        
        fis.close();
        fos.flush();
        fos.close();
        tf.close();
        in.close();
        
        tmpFile.delete();
        retMap.put("flag", "1");
        retMap.put("msg", "Success!");
      }
      catch (Exception e)
      {
        retMap.put("flag", "-1");
        retMap.put("msg", "Failure!" + e.getMessage());
        LOG.error("", e);
      }
    }
    else
    {
      retMap.put("flag", "0");
      retMap.put("msg", "cancel!");
    }
    return retMap;
  }