from src.data.parser import DataParser
from src.utils.constants import XLSX_PATH, CSV_PATH, TACOMETER_VOLTAGE, ARMOR_VOLTAGE, ENGINE_SPEED
from src.params.simulation_params_calculator import SimulationParamsCalculator
from src.params.calculate_motor_controller_params import CalculateMotorControllerParams
from src.utils.logger import AppLogger


def rotine(xlsx_path, csv_path, logger=None):
    if logger is None:
        logger = AppLogger().get_logger()

    xlsx_data = DataParser(xlsx_path, logger)
    csv_data = DataParser(csv_path, logger)

    logger.warning('ANALYZING EXPERIMENT DATA')
    voltage, tachometer, rotation = xlsx_data.linearize_xlsx(ARMOR_VOLTAGE, TACOMETER_VOLTAGE, ENGINE_SPEED)
    logger.info('ARMOR VOLTAGE, TACHOMETER VOLTAGE, AND ENGINE ROTATION DATA EXTRACTED SUCCESSFULLY')

    logger.warning('STARTING DATA ANALYSIS FOR SIMULATION')
    simulation_params = SimulationParamsCalculator(voltage, tachometer, rotation, logger)

    logger.warning('CALCULATING LEAST SQUARES METHOD')
    k_mmq = simulation_params.calculate_k_mmq()

    logger.warning('CALCULATING Kt')
    simulation_params.calculate_kt()

    logger.warning('STARTING AREA METHOD CALCULATION')

    x_axis, y_chanel_one_axis, y_chanel_two_axis = csv_data.parse_csv()
    motor_controller_params = CalculateMotorControllerParams(x_axis, y_chanel_one_axis, y_chanel_two_axis, logger)
    tau, k = motor_controller_params.area_method()

    logger.warning('STARTING CONTROL PARAMETERS CALCULATIONS')

    logger.warning('CALCULATING ZETA AND OMEGA_N')
    zeta = motor_controller_params.calculate_zeta()
    omega_n = motor_controller_params.calculate_omega_n(tau, zeta)

    logger.warning('CALCULATING KP and TI')
    kp = motor_controller_params.calculate_kp(k, tau, zeta, omega_n)
    ti = motor_controller_params.calculate_ti(k, tau, omega_n, kp)
    logger.warning('REPORT SUCCESSFULLY COMPLETED')


if __name__ == '__main__':
    rotine(XLSX_PATH, CSV_PATH)
