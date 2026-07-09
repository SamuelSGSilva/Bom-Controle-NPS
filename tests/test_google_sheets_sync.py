import unittest
from services.google_sheets_sync import converter_linha_para_payload


class GoogleSheetsSyncTests(unittest.TestCase):
    def test_converter_linha_para_payload(self):
        row = [
            "2024-01-01",
            "OS-001",
            "Cliente Teste",
            "SP",
            "Produto A",
            5,
            4,
            3,
            2,
            1,
            5,
            4,
            3,
            2,
            9,
            "Ótimo atendimento",
            4.5,
            "João",
            "Maria",
        ]

        payload, nome_cliente = converter_linha_para_payload(row, 4)

        self.assertEqual(nome_cliente, "Cliente Teste")
        self.assertEqual(payload["numero_os"], "OS-001")
        self.assertEqual(payload["produto_servico"], "Produto A")
        self.assertEqual(payload["nps_score"], 9)
        self.assertEqual(payload["cs_responsavel"], "Maria")
        self.assertEqual(payload["cidade_estado"], "SP")


if __name__ == "__main__":
    unittest.main()
