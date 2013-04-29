import os

dirs=os.listdir('./iso')

f=open('cmip3_bcca.xml', 'w')

for d in dirs:
    ident = d[0:-1-7]
    title = ident.replace('-',' ')
    url = 'http://pcmdi8.llnl.gov/thredds/dodsC/bcca/'+ident
    f.write('<gmd:identificationInfo> <srv:SV_ServiceIdentification id="OPeNDAP"> <gmd:citation> <gmd:CI_Citation> <gmd:title> <gco:CharacterString>'+title+'</gco:CharacterString> </gmd:title> <gmd:date gco:nilReason="missing"/> </gmd:CI_Citation> </gmd:citation> <gmd:abstract gco:nilReason="missing"/> <srv:serviceType> <gco:LocalName>THREDDS OPeNDAP</gco:LocalName> </srv:serviceType> <srv:couplingType> <srv:SV_CouplingType codeList="http://www.tc211.org/ISO19139/resources/codeList.xml#SV_CouplingType" codeListValue="tight">tight</srv:SV_CouplingType> </srv:couplingType> <srv:containsOperations> <srv:SV_OperationMetadata> <srv:operationName> <gco:CharacterString>OPeNDAP Client Access</gco:CharacterString> </srv:operationName> <srv:DCP gco:nilReason="unknown"/> <srv:connectPoint> <gmd:CI_OnlineResource> <gmd:linkage> <gmd:URL>'+url+'</gmd:URL> </gmd:linkage> <gmd:name> <gco:CharacterString>OPeNDAP</gco:CharacterString> </gmd:name> <gmd:description> <gco:CharacterString>THREDDS OPeNDAP</gco:CharacterString> </gmd:description> <gmd:function> <gmd:CI_OnLineFunctionCode codeList="http://www.ngdc.noaa.gov/metadata/published/xsd/schema/resources/Codelist/gmxCodelists.xml#CI_OnLineFunctionCode" codeListValue="download">download</gmd:CI_OnLineFunctionCode> </gmd:function> </gmd:CI_OnlineResource> </srv:connectPoint> </srv:SV_OperationMetadata> </srv:containsOperations> <srv:operatesOn xlink:href="#DataIdentification"/> </srv:SV_ServiceIdentification> </gmd:identificationInfo>\n')

f.close()