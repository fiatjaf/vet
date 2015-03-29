-- ----------------------------------------------------------
-- MDB Tools - A library for reading MS Access database files
-- Copyright (C) 2000-2011 Brian Bruns and others.
-- Files in libmdb are licensed under LGPL and the utilities under
-- the GPL, see COPYING.LIB and COPYING files respectively.
-- Check out http://mdbtools.sourceforge.net
-- ----------------------------------------------------------

CREATE TABLE "CATEGORIA PRODUTO"
 (
	"CodigoCategoria"			INTEGER PRIMARY KEY, 
	"NomeCategoria"			VARCHAR (100)
);


CREATE TABLE "CLIENTE"
 (
	"CodigoCliente"			INTEGER PRIMARY KEY, 
	"NomeCliente"			VARCHAR (100), 
	"ReferenciaCliente"			VARCHAR (60), 
	"RuaCliente"			VARCHAR (80), 
	"BairroCliente"			VARCHAR (60), 
	"CidadeCliente"			VARCHAR (60), 
	"CepCliente"			VARCHAR (30), 
	"FonreResidencialCliente"			VARCHAR (30), 
	"FoneComercialCliente"			VARCHAR (30), 
	"ComplementeCliente"			TEXT, 
	"TipoEndCliente"			VARCHAR (2), 
	"FoneCelular"			VARCHAR (30)
);

-- CREATE INDEXES ...
CREATE INDEX "CLIENTE_NomeCliente_idx" ON "CLIENTE" ("NomeCliente");


CREATE TABLE "COBRANCA"
 (
	"codigoserv"			INTEGER PRIMARY KEY, 
	"histórico"			TEXT, 
	"valor"			DOUBLE PRECISION, 
	"data"			DATE, 
	"codigoocorrencia"			INTEGER, 
	"codigocliente"			INTEGER
);


CREATE TABLE "COR"
 (
	"CodigoCor"			INTEGER PRIMARY KEY, 
	"NomeCor"			VARCHAR (40)
);

-- CREATE INDEXES ...
CREATE INDEX "COR_NomeCor_idx" ON "COR" ("NomeCor");


CREATE TABLE "DIAGNOSTICO"
 (
	"CodigoDiagnostico"			INTEGER PRIMARY KEY, 
	"DescricaoDiagnostico"			VARCHAR (120)
);


CREATE TABLE "DISTRIBUIDOR PRODUTO"
 (
	"CodigoDistribuidor"			INTEGER PRIMARY KEY, 
	"NomeDistribuidor"			VARCHAR (100), 
	"EnderecoDistribuidor"			VARCHAR (100), 
	"CidadeDistribuidor"			VARCHAR (100), 
	"CepDistribuidor"			VARCHAR (100), 
	"EstadoDistribuidor"			VARCHAR (100), 
	"Fone1Distribuidor"			VARCHAR (100), 
	"Fone2Distribuidor"			VARCHAR (100), 
	"FaxDistribuidor"			VARCHAR (100), 
	"ContatoDistribuidor"			VARCHAR (100)
);


CREATE TABLE "DOENCA"
 (
	"CodigoDoença"			INTEGER PRIMARY KEY, 
	"NomeDoença"			VARCHAR (60)
);


CREATE TABLE "ESPECIE"
 (
	"CodigoEspecie"			INTEGER PRIMARY KEY, 
	"NomeEspecie"			VARCHAR (40), 
	"AdjetivoMalaDireta"			VARCHAR (100)
);


CREATE TABLE "FABRICANTE PRODUTO"
 (
	"CodigoFabricante"			INTEGER PRIMARY KEY, 
	"NomeFabricante"			VARCHAR (100)
);


CREATE TABLE "FABRICANTE VACINA"
 (
	"CodigoFabricante"			INTEGER PRIMARY KEY, 
	"NomeFabricante"			VARCHAR (100)
);


CREATE TABLE "lixo1"
 (
	"CodigoPaciente"			INTEGER PRIMARY KEY, 
	"MáxDeDataAtendimento"			DATE
);

CREATE TABLE "MOVIMENTO PRODUTO"
 (
	"NumeroMovimento"			INTEGER PRIMARY KEY, 
	"CódigoProduto"			INTEGER, 
	"MovimentoData"			DATE, 
	"EntradaSaída"			VARCHAR (2), 
	"TipoMovimento"			INTEGER, 
	"QuantidadeMovimentada"			DOUBLE PRECISION, 
	"HistoricoMovimentacao"			TEXT, 
	"ValorMovimento"			DOUBLE PRECISION, 
	"QuantidadeAnterior"			DOUBLE PRECISION, 
	"EntradaSaídaAnterior"			VARCHAR (2)
);

-- CREATE INDEXES ...
CREATE INDEX "MOVIMENTO PRODUTO_CódigoProduto_idx" ON "MOVIMENTO PRODUTO" ("CódigoProduto");


CREATE TABLE "OCORRENCIA"
 (
	"CodigoOcorrencia"			INTEGER PRIMARY KEY, 
	"DescricaoOcorrencia"			VARCHAR (40)
);


CREATE TABLE "PRODUTO"
 (
	"CodigoProduto"			INTEGER PRIMARY KEY, 
	"NomeProduto"			VARCHAR (100), 
	"UnidadeProduto"			VARCHAR (100), 
	"DescricaoProduto"			TEXT, 
	"PrecoProduto"			DOUBLE PRECISION, 
	"FabricanteProduto"			INTEGER, 
	"CategoriaProduto"			INTEGER, 
	"DistribuidorProduto"			INTEGER, 
	"QuantidadeEstoque"			DOUBLE PRECISION, 
	"EstoqueMínimo"			DOUBLE PRECISION, 
	"EstoqueMáximo"			DOUBLE PRECISION, 
	"PropriedadeProduto"			INTEGER
);


CREATE TABLE "PRODUTO1"
 (
	"CodigoProduto"			INTEGER PRIMARY KEY, 
	"NomeProduto"			VARCHAR (100), 
	"UnidadeProduto"			VARCHAR (100), 
	"DescricaoProduto"			TEXT, 
	"PrecoProduto"			DOUBLE PRECISION, 
	"FabricanteProduto"			INTEGER, 
	"CategoriaProduto"			INTEGER, 
	"DistribuidorProduto"			INTEGER, 
	"QuantidadeEstoque"			DOUBLE PRECISION, 
	"EstoqueMínimo"			DOUBLE PRECISION, 
	"EstoqueMáximo"			DOUBLE PRECISION, 
	"PropriedadeProduto"			INTEGER
);


CREATE TABLE "PROPRIEDADE PRODUTO"
 (
	"CodigoPropriedade"			INTEGER PRIMARY KEY, 
	"DescricaoPropriedade"			VARCHAR (100)
);


CREATE TABLE "RACA"
 (
	"CodigoEspecie"			INTEGER, 
	"CodigoRaca"			INTEGER, 
	"NomeRaca"			VARCHAR (100),
    UNIQUE ("CodigoEspecie", "CodigoRaca")
);


CREATE TABLE "SUBDIAGNOSTICO"
 (
	"CodigoDiagnostico"			INTEGER, 
	"CodigoSubDiagnostico"			INTEGER PRIMARY KEY, 
	"DescricaoSubDiagnostico"			VARCHAR (120)
);


CREATE TABLE "TIPO MOVIMENTO PRODUTO"
 (
	"CodigoTipoMovimento"			INTEGER PRIMARY KEY, 
	"DescricaoTipoMovimento"			VARCHAR (100)
);


CREATE TABLE "TIPO VACINA"
 (
	"CodigoTipoVacina"			INTEGER PRIMARY KEY, 
	"DescriçãoTipoVacina"			VARCHAR (100)
);


CREATE TABLE "TIPO VACINA x DOENÇA"
 (
	"CodigoTipoVacina"			INTEGER, 
	"CodigoDoença"			INTEGER
);


CREATE TABLE "UNIDADE"
 (
	"SiglaUnidade"			VARCHAR (100), 
	"NomeUnidade"			VARCHAR (100)
);


CREATE TABLE "VACINA APLICADA"
 (
	"CodigoPaciente"			INTEGER, 
	"DataVacinacao"			DATE, 
	"CodigoTipoVacina"			INTEGER, 
	"HistoricoVacinacao"			TEXT, 
	"CodigoFabricante"			INTEGER, 
	"PartidaVacina"			VARCHAR (100)
);


CREATE TABLE "VACINA PLANEJADA"
 (
	"CodigoPaciente"			INTEGER, 
	"DataVacinacao"			DATE, 
	"CodigoTipoVacina"			INTEGER
);


CREATE TABLE "ATENDIMENTO"
 (
	"NumeroAtendimento"			INTEGER PRIMARY KEY, 
	"CodigoPaciente"			INTEGER, 
	"DataAtendimento"			DATE DEFAULT CURRENT_TIMESTAMP, 
	"CodigoOcorrencia"			INTEGER, 
	"CodigoDiagnostico"			INTEGER, 
	"CodigoSubDiagnostico"			INTEGER, 
	"Historico"			TEXT, 
	"ValorAtendimento"			REAL, 
	"QuitacaoAtendimento"			VARCHAR (2)
);


CREATE TABLE "PACIENTE"
 (
	"CodigoPaciente"			INTEGER PRIMARY KEY, 
	"CodigoPlanoVacinacao"			INTEGER, 
	"SexoPaciente"			VARCHAR (2), 
	"CorPaciente"			INTEGER REFERENCES COR(CodigoCor), 
	"NascimentoPaciente"			DATE, 
	"FalecimentoPaciente"			DATE, 
	"CausaFalecimentoPaciente"			DOUBLE PRECISION, 
	"ClientePaciente"			INTEGER, 
	"CadastramentoPaciente"			DATE, 
	"ObservaçaoPaciente"			TEXT, 
	"PedigreePaciente"			VARCHAR (2), 
	"StatusPaciente"			VARCHAR (2), 
	"NomePaciente"			VARCHAR (40), 
	"CruzamentoPaciente"			VARCHAR (2), 
	"EspeciePaciente"			INTEGER, 
	"RacaPaciente"			INTEGER, 
	"SelecaoVacinacao"			VARCHAR (2)
);
